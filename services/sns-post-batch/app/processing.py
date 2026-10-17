"""SNS account processing and post state persistence."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any, Callable

from acps_shared import (
    InstagramApiError,
    InstagramTransportError,
    build_sns_secret_name,
    generate_presigned_url,
    get_secret_string,
    parse_sns_secret,
)

from .instagram_api import (
    InstagramResultUnknown,
    create_container,
    get_container_status,
    is_transient_api_error,
    poll_container_status,
    publish_container,
    resolve_poll_settings,
)
from .media_types import MEDIA_TYPE_REEL, MEDIA_TYPE_STORY, derive_media_type
from .models import CaptionTemplate, GeneratedMediaRef, SnsAccount
from .post_media import ensure_post_media
from .problem_snapshot import write_problem_snapshot
from .posts import (
    create_pending_post,
    get_post,
    update_post_container_created,
    update_post_failed,
    update_post_snapshot,
    update_post_success,
    update_post_unconfirmed,
)


logger = logging.getLogger(__name__)

TERMINAL_POST_STATUSES = {"success", "failed", "published_unconfirmed"}
PUBLISH_CHECK_DELAY_SECONDS = 10.0


@dataclass(frozen=True)
class ProcessingResult:
    """Result of processing all active SNS accounts."""

    accounts_processed: int
    all_accounts_success: bool


@dataclass
class _RecoveryState:
    """Keep bounded recovery history for one posts row in task memory."""

    first_error: dict[str, Any] | None = None
    container_check: dict[str, Any] | None = None
    creation_retried: bool = False
    publish_retried: bool = False

    def remember_first_error(
        self,
        stage: str,
        container_id: str | None,
        exc: InstagramApiError,
    ) -> None:
        """Retain the first failure even when both recovery paths are used."""
        if self.first_error is None:
            response = exc.response
            if response is None and isinstance(exc, InstagramTransportError):
                response = {"transport_error": str(exc)}
            self.first_error = {
                "stage": stage,
                "container_id": container_id,
                "response": response,
            }

    def api_response(
        self,
        response: dict[str, Any] | None,
        *,
        success: bool = False,
    ) -> dict[str, Any] | None:
        """Wrap diagnostics only for rows that needed recovery."""
        if self.first_error is None:
            return response
        return {
            "final": None if success else response,
            "first_error": self.first_error,
            "container_check": self.container_check,
        }

    def error_message(self, message: str) -> str:
        """Annotate the final failure with the recovery attempts used."""
        if self.creation_retried:
            message += "（作成から 1 回やり直し済み）"
        if self.publish_retried:
            message += "（公開を 1 回再送済み）"
        return message


def _publish_with_recovery(
    access_token: str,
    ig_user_id: str,
    container_id: str,
    *,
    recovery: _RecoveryState,
    urlopen: Any,
    sleep: Callable[[float], None],
) -> tuple[str, dict[str, Any]]:
    """Check a transient publish failure once and resend only if FINISHED."""
    try:
        return publish_container(
            access_token, ig_user_id, container_id, urlopen=urlopen
        )
    except InstagramApiError as exc:
        if not is_transient_api_error(exc):
            raise
        recovery.remember_first_error("publish", container_id, exc)
        sleep(PUBLISH_CHECK_DELAY_SECONDS)
        try:
            recovery.container_check = get_container_status(
                access_token, container_id, urlopen=urlopen
            )
        except Exception as check_exc:
            raise InstagramResultUnknown(
                str(check_exc), response=getattr(check_exc, "response", None)
            ) from check_exc

        status_code = recovery.container_check.get("status_code")
        if status_code != "FINISHED":
            message = str(exc)
            if status_code == "PUBLISHED":
                message = f"PUBLISHED 確認済み: {message}"
            raise InstagramResultUnknown(message, response=exc.response) from exc

    # Publishing is outside the creation loop: never replace this container.
    recovery.publish_retried = True
    try:
        return publish_container(
            access_token, ig_user_id, container_id, urlopen=urlopen
        )
    except InstagramApiError as exc:
        if is_transient_api_error(exc):
            raise InstagramResultUnknown(str(exc), response=exc.response) from exc
        raise


def _rollback_safely(connection: Any) -> None:
    """Roll back uncommitted DB work without masking the original error."""
    rollback = getattr(connection, "rollback", None)
    if callable(rollback):
        try:
            rollback()
        except Exception:
            logger.exception("投稿処理のロールバックに失敗")


def _record_request_failure(
    cursor: Any,
    connection: Any,
    *,
    post_id: int,
    error_message: str,
    api_response: dict[str, Any] | None,
    unconfirmed: bool,
) -> None:
    """Persist a classified API failure and commit it."""
    if unconfirmed:
        update_post_unconfirmed(
            cursor,
            post_id,
            error_message=error_message,
            api_response=api_response,
        )
    else:
        update_post_failed(
            cursor,
            post_id,
            error_message=error_message,
            api_response=api_response,
        )
    connection.commit()


def _process_account_media(
    cursor: Any,
    connection: Any,
    *,
    set_id: int,
    generation_run_id: int,
    account: SnsAccount,
    caption_template: CaptionTemplate | None,
    caption_text: str,
    generated_media: GeneratedMediaRef,
    media_type: str,
    save_caption_snapshot: bool,
    problem_snapshot_enabled: bool,
    env_name: str,
    set_code: str,
    s3_bucket: str,
    s3_client: Any,
    urlopen: Any,
    sleep: Callable[[float], None],
    on_attempt: Callable[[], None] | None = None,
) -> bool:
    """Process one account and media type, returning whether it is successful."""
    try:
        post = get_post(
            cursor,
            generation_run_id,
            account.id,
            media_type=media_type,
        )
    except Exception:
        logger.exception(
            "投稿状態の取得に失敗: sns_account_id=%s media_type=%s",
            account.id,
            media_type,
        )
        return False

    if post is not None and post.status in TERMINAL_POST_STATUSES:
        logger.info(
            "終端状態のためスキップ: post_id=%s sns_account_id=%s media_type=%s",
            post.id,
            account.id,
            media_type,
        )
        return post.status == "success"

    if on_attempt is not None:
        on_attempt()
    logger.info(
        "投稿処理を開始: sns_account_id=%s media_type=%s",
        account.id,
        media_type,
    )
    post_id: int | None = post.id if post is not None else None
    recovery = _RecoveryState()
    try:
        if post is None:
            post_id = create_pending_post(
                cursor,
                set_id=set_id,
                generation_run_id=generation_run_id,
                sns_account_id=account.id,
                media_type=media_type,
            )
            ensure_post_media(
                cursor,
                post_id=post_id,
                generated_media_id=generated_media.id,
            )

        if save_caption_snapshot:
            update_post_snapshot(
                cursor,
                post_id,
                caption_template_id=(
                    caption_template.id if caption_template is not None else None
                ),
                caption_text=caption_text,
                media_type=media_type,
            )
        connection.commit()

        if account.platform != "instagram":
            logger.warning(
                "未対応の SNS プラットフォームをスキップ: "
                "platform=%s sns_account_id=%s",
                account.platform,
                account.id,
            )
            return False

        secret_name = build_sns_secret_name(
            env_name,
            set_code,
            account.platform,
            account.account_code,
        )
        credentials = parse_sns_secret(get_secret_string(secret_name))

        container_id = None
        if (
            post is not None
            and post.status == "container_created"
            and post.platform_container_id
        ):
            container_id = post.platform_container_id

        poll_settings = resolve_poll_settings(media_type)
        while True:
            stage = "create" if container_id is None else "poll"
            try:
                if container_id is None:
                    media_url = generate_presigned_url(
                        s3_bucket,
                        generated_media.s3_key,
                        expires_in=3600,
                        client=s3_client,
                    )
                    caption_args = (caption_text,) if save_caption_snapshot else ()
                    container_id, _ = create_container(
                        credentials.access_token,
                        credentials.ig_user_id,
                        media_url,
                        *caption_args,
                        media_type=media_type,
                        urlopen=urlopen,
                    )
                    update_post_container_created(
                        cursor,
                        post_id,
                        platform_container_id=container_id,
                    )
                    connection.commit()

                stage = "poll"
                poll_container_status(
                    credentials.access_token,
                    container_id,
                    urlopen=urlopen,
                    max_attempts=poll_settings.max_attempts,
                    poll_interval_seconds=poll_settings.interval_seconds,
                )
                break
            except InstagramApiError as exc:
                processing_error = (
                    stage == "poll"
                    and isinstance(exc.response, dict)
                    and exc.response.get("status_code") == "ERROR"
                )
                transient = (
                    processing_error
                    or isinstance(exc, InstagramTransportError)
                    or is_transient_api_error(exc)
                )
                if recovery.creation_retried or not transient:
                    raise
                recovery.remember_first_error(stage, container_id, exc)
                recovery.creation_retried = True
                logger.warning(
                    "投稿コンテナを作成からやり直す: "
                    "post_id=%s container_id=%s stage=%s error=%s",
                    post_id,
                    container_id,
                    stage,
                    exc,
                )
                container_id = None

        platform_post_id, api_response = _publish_with_recovery(
            credentials.access_token,
            credentials.ig_user_id,
            container_id,
            recovery=recovery,
            urlopen=urlopen,
            sleep=sleep,
        )
        posted_at = update_post_success(
            cursor,
            post_id,
            platform_post_id=platform_post_id,
            api_response=recovery.api_response(api_response, success=True),
        )
        connection.commit()
        if problem_snapshot_enabled and media_type == MEDIA_TYPE_REEL:
            try:
                write_problem_snapshot(
                    cursor,
                    connection,
                    set_id=set_id,
                    set_code=set_code,
                    generation_run_id=generation_run_id,
                    media_id=platform_post_id,
                    posted_at=posted_at,
                    s3_bucket=s3_bucket,
                    s3_client=s3_client,
                )
            except Exception:
                logger.warning(
                    "問題スナップショットの出力に失敗: "
                    "generation_run_id=%s media_id=%s",
                    generation_run_id,
                    platform_post_id,
                    exc_info=True,
                )
                _rollback_safely(connection)
        return True
    except InstagramResultUnknown as exc:
        logger.error(
            "Instagram API の結果が不明: sns_account_id=%s media_type=%s error=%s",
            account.id,
            media_type,
            exc,
        )
        if post_id is not None:
            try:
                _record_request_failure(
                    cursor,
                    connection,
                    post_id=post_id,
                    error_message=recovery.error_message(str(exc)),
                    api_response=recovery.api_response(exc.response),
                    unconfirmed=True,
                )
            except Exception:
                logger.exception(
                    "published_unconfirmed 状態の保存に失敗: post_id=%s",
                    post_id,
                )
                _rollback_safely(connection)
        return False
    except InstagramApiError as exc:
        logger.error(
            "Instagram API が明確な失敗を返却: "
            "sns_account_id=%s media_type=%s error=%s",
            account.id,
            media_type,
            exc,
        )
        if post_id is not None:
            try:
                _record_request_failure(
                    cursor,
                    connection,
                    post_id=post_id,
                    error_message=recovery.error_message(str(exc)),
                    api_response=recovery.api_response(exc.response),
                    unconfirmed=False,
                )
            except Exception:
                logger.exception("failed 状態の保存に失敗: post_id=%s", post_id)
                _rollback_safely(connection)
        return False
    except Exception:
        logger.exception(
            "SNS アカウント処理で予期しないエラー: "
            "sns_account_id=%s media_type=%s",
            account.id,
            media_type,
        )
        _rollback_safely(connection)
        return False


def process_target_generation_run(
    cursor: Any,
    connection: Any,
    *,
    set_id: int,
    generation_run_id: int,
    sns_accounts: list[SnsAccount],
    caption_template: CaptionTemplate | None,
    generated_media: GeneratedMediaRef,
    stories_enabled: bool = False,
    problem_snapshot_enabled: bool = False,
    env_name: str,
    set_code: str,
    s3_bucket: str,
    s3_client: Any,
    urlopen: Any,
    caption_text: str | None = None,
    sleep: Callable[[float], None] | None = None,
) -> ProcessingResult:
    """Process one generated media item for each active SNS account.

    Terminal post states are skipped. Each non-terminal account is attempted
    independently, and a final database recheck determines overall success.
    """
    attempted_account_ids: set[int] = set()
    if sleep is None:
        sleep = time.sleep
    if caption_text is None:
        caption_text = caption_template.template_text if caption_template else ""
    media_type = derive_media_type(generated_media.file_format)

    for account in sns_accounts:
        primary_success = _process_account_media(
            cursor,
            connection,
            set_id=set_id,
            generation_run_id=generation_run_id,
            account=account,
            caption_template=caption_template,
            caption_text=caption_text,
            generated_media=generated_media,
            media_type=media_type,
            save_caption_snapshot=True,
            problem_snapshot_enabled=problem_snapshot_enabled,
            env_name=env_name,
            set_code=set_code,
            s3_bucket=s3_bucket,
            s3_client=s3_client,
            urlopen=urlopen,
            sleep=sleep,
            on_attempt=lambda account_id=account.id: attempted_account_ids.add(
                account_id
            ),
        )
        if stories_enabled and media_type == MEDIA_TYPE_REEL and primary_success:
            _process_account_media(
                cursor,
                connection,
                set_id=set_id,
                generation_run_id=generation_run_id,
                account=account,
                caption_template=None,
                caption_text="",
                generated_media=generated_media,
                media_type=MEDIA_TYPE_STORY,
                save_caption_snapshot=False,
                problem_snapshot_enabled=False,
                env_name=env_name,
                set_code=set_code,
                s3_bucket=s3_bucket,
                s3_client=s3_client,
                urlopen=urlopen,
                sleep=sleep,
                on_attempt=lambda account_id=account.id: attempted_account_ids.add(
                    account_id
                ),
            )

    all_accounts_success = True
    for account in sns_accounts:
        final_post = get_post(
            cursor,
            generation_run_id,
            account.id,
            media_type=media_type,
        )
        if final_post is None or final_post.status != "success":
            all_accounts_success = False
            continue
        if stories_enabled and media_type == MEDIA_TYPE_REEL:
            final_story = get_post(
                cursor,
                generation_run_id,
                account.id,
                media_type=MEDIA_TYPE_STORY,
            )
            if final_story is None or final_story.status != "success":
                all_accounts_success = False

    return ProcessingResult(len(attempted_account_ids), all_accounts_success)
