"""SNS account processing and post state persistence."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Callable

from acps_shared import generate_presigned_url, get_secret_string

from .instagram_api import (
    InstagramRequestFailed,
    InstagramResultUnknown,
    create_container,
    poll_container_status,
    publish_container,
    resolve_poll_settings,
)
from .media_types import MEDIA_TYPE_REEL, MEDIA_TYPE_STORY, derive_media_type
from .models import CaptionTemplate, GeneratedMediaRef, SnsAccount
from .post_media import ensure_post_media
from .posts import (
    create_pending_post,
    get_post,
    update_post_container_created,
    update_post_failed,
    update_post_snapshot,
    update_post_success,
    update_post_unconfirmed,
)
from .secrets import build_sns_secret_name, parse_sns_secret


logger = logging.getLogger(__name__)

TERMINAL_POST_STATUSES = {"success", "failed", "published_unconfirmed"}


@dataclass(frozen=True)
class ProcessingResult:
    """Result of processing all active SNS accounts."""

    accounts_processed: int
    all_accounts_success: bool


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
    env_name: str,
    set_code: str,
    s3_bucket: str,
    s3_client: Any,
    urlopen: Any,
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

        if (
            post is not None
            and post.status == "container_created"
            and post.platform_container_id
        ):
            container_id = post.platform_container_id
        else:
            media_url = generate_presigned_url(
                s3_bucket,
                generated_media.s3_key,
                expires_in=3600,
                client=s3_client,
            )
            if save_caption_snapshot:
                container_id, _ = create_container(
                    credentials.access_token,
                    credentials.ig_user_id,
                    media_url,
                    caption_text,
                    media_type=media_type,
                    urlopen=urlopen,
                )
            else:
                container_id, _ = create_container(
                    credentials.access_token,
                    credentials.ig_user_id,
                    media_url,
                    media_type=media_type,
                    urlopen=urlopen,
                )
            update_post_container_created(
                cursor,
                post_id,
                platform_container_id=container_id,
            )
            connection.commit()

        poll_settings = resolve_poll_settings(media_type)
        poll_container_status(
            credentials.access_token,
            container_id,
            urlopen=urlopen,
            max_attempts=poll_settings.max_attempts,
            poll_interval_seconds=poll_settings.interval_seconds,
        )
        platform_post_id, api_response = publish_container(
            credentials.access_token,
            credentials.ig_user_id,
            container_id,
            urlopen=urlopen,
        )
        update_post_success(
            cursor,
            post_id,
            platform_post_id=platform_post_id,
            api_response=api_response,
        )
        connection.commit()
        return True
    except InstagramRequestFailed as exc:
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
                    error_message=str(exc),
                    api_response=exc.response,
                    unconfirmed=False,
                )
            except Exception:
                logger.exception("failed 状態の保存に失敗: post_id=%s", post_id)
                _rollback_safely(connection)
        return False
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
                    error_message=str(exc),
                    api_response=exc.response,
                    unconfirmed=True,
                )
            except Exception:
                logger.exception(
                    "published_unconfirmed 状態の保存に失敗: post_id=%s",
                    post_id,
                )
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
    env_name: str,
    set_code: str,
    s3_bucket: str,
    s3_client: Any,
    urlopen: Any,
    caption_text: str | None = None,
) -> ProcessingResult:
    """Process one generated media item for each active SNS account.

    Terminal post states are skipped. Each non-terminal account is attempted
    independently, and a final database recheck determines overall success.
    """
    attempted_account_ids: set[int] = set()
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
            env_name=env_name,
            set_code=set_code,
            s3_bucket=s3_bucket,
            s3_client=s3_client,
            urlopen=urlopen,
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
                env_name=env_name,
                set_code=set_code,
                s3_bucket=s3_bucket,
                s3_client=s3_client,
                urlopen=urlopen,
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
