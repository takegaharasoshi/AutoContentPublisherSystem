"""SNS account processing and post state persistence."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from acps_shared import generate_presigned_url, get_secret_string

from .instagram_api import (
    InstagramRequestFailed,
    InstagramResultUnknown,
    create_container,
    poll_container_status,
    publish_container,
)
from .models import CaptionTemplate, GeneratedImageRef, SnsAccount
from .post_images import ensure_post_image
from .posts import (
    create_pending_post,
    get_post,
    update_post_caption,
    update_post_container_created,
    update_post_failed,
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


def process_target_generation_run(
    cursor: Any,
    connection: Any,
    *,
    set_id: int,
    generation_run_id: int,
    sns_accounts: list[SnsAccount],
    caption_template: CaptionTemplate | None,
    generated_image: GeneratedImageRef,
    env_name: str,
    set_code: str,
    s3_bucket: str,
    s3_client: Any,
    urlopen: Any,
) -> ProcessingResult:
    """Process one generated image for each active SNS account.

    Terminal post states are skipped. Each non-terminal account is attempted
    independently, and a final database recheck determines overall success.
    """
    accounts_processed = 0
    caption_text = caption_template.template_text if caption_template else ""

    for account in sns_accounts:
        try:
            post = get_post(cursor, generation_run_id, account.id)
        except Exception:
            logger.exception(
                "投稿状態の取得に失敗: sns_account_id=%s", account.id
            )
            continue

        if post is not None and post.status in TERMINAL_POST_STATUSES:
            logger.info(
                "終端状態のためスキップ: post_id=%s sns_account_id=%s",
                post.id,
                account.id,
            )
            continue

        accounts_processed += 1
        post_id: int | None = post.id if post is not None else None
        try:
            if post is None:
                post_id = create_pending_post(
                    cursor,
                    set_id=set_id,
                    generation_run_id=generation_run_id,
                    sns_account_id=account.id,
                )
                ensure_post_image(
                    cursor,
                    post_id=post_id,
                    generated_image_id=generated_image.id,
                )

            update_post_caption(
                cursor,
                post_id,
                caption_template_id=caption_template.id if caption_template else None,
                caption_text=caption_text,
            )
            connection.commit()

            if account.platform != "instagram":
                logger.warning(
                    "未対応の SNS プラットフォームをスキップ: "
                    "platform=%s sns_account_id=%s",
                    account.platform,
                    account.id,
                )
                continue

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
                image_url = generate_presigned_url(
                    s3_bucket,
                    generated_image.s3_key,
                    expires_in=3600,
                    client=s3_client,
                )
                container_id, _ = create_container(
                    credentials.access_token,
                    credentials.ig_user_id,
                    image_url,
                    caption_text,
                    urlopen=urlopen,
                )
                update_post_container_created(
                    cursor,
                    post_id,
                    platform_container_id=container_id,
                )
                connection.commit()

            poll_container_status(
                credentials.access_token,
                container_id,
                urlopen=urlopen,
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
        except InstagramRequestFailed as exc:
            logger.error(
                "Instagram API が明確な失敗を返却: "
                "sns_account_id=%s error=%s",
                account.id,
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
                    logger.exception(
                        "failed 状態の保存に失敗: post_id=%s", post_id
                    )
                    _rollback_safely(connection)
        except InstagramResultUnknown as exc:
            logger.error(
                "Instagram API の結果が不明: sns_account_id=%s error=%s",
                account.id,
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
        except Exception:
            logger.exception(
                "SNS アカウント処理で予期しないエラー: sns_account_id=%s",
                account.id,
            )
            _rollback_safely(connection)

    all_accounts_success = True
    for account in sns_accounts:
        final_post = get_post(cursor, generation_run_id, account.id)
        if final_post is None or final_post.status != "success":
            all_accounts_success = False

    return ProcessingResult(accounts_processed, all_accounts_success)
