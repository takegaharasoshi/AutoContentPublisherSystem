"""Instagram コメント Webhook PoC 用 Lambda ハンドラ。"""

import base64
import hashlib
import hmac
import json
import logging
import os
from collections.abc import Mapping
from typing import Any
from urllib import parse, request

import boto3


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

GRAPH_API_BASE = os.environ.get("GRAPH_API_BASE", "https://graph.instagram.com/v23.0")
OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
FALLBACK_REPLY = "「はい / いいえ」で答えられる質問をコメントしてね！"
SYSTEM_PROMPT = """あなたはウミガメのスープの出題者です。

サンプル問題:
問題: ある男がレストランで「ウミガメのスープ」を注文し、一口飲んで店を出た後、自殺した。なぜ？
真相: 男は過去に遭難して仲間からウミガメのスープだと言われた肉を食べて生き延びたが、実際には人肉だった。レストランで本物の味を知り、真相を悟った。

ユーザーの質問には「はい」「いいえ」「関係ありません」を中心に短い日本語で答えてください。真相は直接明かさないでください。"""

_secrets_cache: dict[str, str] | None = None


def response(status_code: int, body: str = "", content_type: str = "text/plain") -> dict[str, Any]:
    """Lambda Function URL 形式のレスポンスを返す。"""
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": content_type},
        "body": body,
    }


def get_secrets() -> dict[str, str]:
    """Secrets Manager から認証情報を取得し、実行環境内でキャッシュする。"""
    global _secrets_cache
    if _secrets_cache is not None:
        return _secrets_cache

    secret_arn = os.environ["SECRET_ARN"]
    result = boto3.client("secretsmanager").get_secret_value(SecretId=secret_arn)
    secret_string = result["SecretString"]
    parsed = json.loads(secret_string)
    if not isinstance(parsed, dict):
        raise ValueError("SecretString must be a JSON object")

    _secrets_cache = {
        key: str(parsed.get(key, ""))
        for key in (
            "verify_token",
            "app_secret",
            "ig_access_token",
            "ig_user_id",
            "openai_api_key",
        )
    }
    return _secrets_cache


def get_raw_body(event: Mapping[str, Any]) -> bytes:
    """Function URL イベントから、署名検証対象の元のリクエスト本文を取得する。"""
    body = event.get("body", "")
    if body is None:
        body = ""
    if not isinstance(body, str):
        raise ValueError("Request body must be a string")
    if event.get("isBase64Encoded"):
        return base64.b64decode(body, validate=True)
    return body.encode("utf-8")


def get_header(headers: Mapping[str, Any] | None, name: str) -> str:
    """大文字小文字を区別せずに HTTP ヘッダを取り出す。"""
    for key, value in (headers or {}).items():
        if key.lower() == name.lower():
            return str(value)
    return ""


def is_valid_signature(signature_header: str, raw_body: bytes, app_secret: str) -> bool:
    """Meta の sha256 署名を検証する。"""
    prefix = "sha256="
    if not signature_header.startswith(prefix):
        return False
    expected = hmac.new(
        app_secret.encode("utf-8"), raw_body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature_header[len(prefix) :], expected)


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str]) -> str:
    """JSON を POST し、レスポンス本文を文字列で返す。"""
    encoded = json.dumps(payload).encode("utf-8")
    http_request = request.Request(url, data=encoded, headers=headers, method="POST")
    with request.urlopen(http_request, timeout=20) as http_response:
        return http_response.read().decode("utf-8")


def post_form(url: str, payload: Mapping[str, str]) -> str:
    """フォーム形式のデータを POST し、レスポンス本文を文字列で返す。"""
    encoded = parse.urlencode(payload).encode("utf-8")
    http_request = request.Request(
        url,
        data=encoded,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with request.urlopen(http_request, timeout=20) as http_response:
        return http_response.read().decode("utf-8")


def generate_reply(comment_text: str, openai_api_key: str) -> str:
    """OpenAI を使って短い出題者回答を生成し、失敗時は固定文言へフォールバックする。"""
    if not openai_api_key:
        return FALLBACK_REPLY

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": comment_text},
        ],
    }
    try:
        result = json.loads(
            post_json(
                OPENAI_CHAT_COMPLETIONS_URL,
                payload,
                {
                    "Authorization": f"Bearer {openai_api_key}",
                    "Content-Type": "application/json",
                },
            )
        )
        content = result["choices"][0]["message"]["content"]
        if not isinstance(content, str) or not content.strip():
            raise ValueError("OpenAI response did not include message content")
        return content[:500]
    except Exception as exc:
        LOGGER.warning("OpenAI 呼び出しに失敗したため固定文言へフォールバックします: %s", exc)
        return FALLBACK_REPLY


def reply_to_comment(comment_id: str, message: str, secrets: Mapping[str, str]) -> str:
    """Graph API を通じてコメントへ返信する。"""
    url = f"{GRAPH_API_BASE.rstrip('/')}/{comment_id}/replies"
    return post_form(
        url,
        {"message": message, "access_token": secrets["ig_access_token"]},
    )


def process_comment(value: Mapping[str, Any], secrets: Mapping[str, str]) -> None:
    """1 件のコメントイベントを処理する。"""
    comment_id = str(value.get("id", ""))
    comment_text = str(value.get("text", ""))
    sender = value.get("from")
    sender = sender if isinstance(sender, Mapping) else {}
    sender_id = str(sender.get("id", ""))
    sender_username = str(sender.get("username", ""))
    media = value.get("media")
    media = media if isinstance(media, Mapping) else {}
    media_id = str(media.get("id", value.get("media_id", "")))

    if sender_id == secrets["ig_user_id"]:
        LOGGER.info("自分の返信コメントをスキップしました: comment_id=%s", comment_id)
        return
    if not comment_id:
        LOGGER.warning("comment id がないためコメントをスキップしました: %s", value)
        return

    LOGGER.info(
        "コメントを処理します: comment_id=%s sender_id=%s username=%s media_id=%s",
        comment_id,
        sender_id,
        sender_username,
        media_id,
    )
    message = generate_reply(comment_text, secrets["openai_api_key"])
    result = reply_to_comment(comment_id, message, secrets)
    LOGGER.info("Graph API 返信結果: comment_id=%s response=%s", comment_id, result)


def process_comment_changes(payload: Mapping[str, Any], secrets: Mapping[str, str]) -> None:
    """ペイロード内の comments フィールドを個別に処理する。"""
    entries = payload.get("entry", [])
    if not isinstance(entries, list):
        return
    for entry in entries:
        if not isinstance(entry, Mapping):
            continue
        changes = entry.get("changes", [])
        if not isinstance(changes, list):
            continue
        for change in changes:
            if not isinstance(change, Mapping) or change.get("field") != "comments":
                continue
            value = change.get("value", {})
            if not isinstance(value, Mapping):
                LOGGER.warning("comments の value がオブジェクトではありません: %s", value)
                continue
            try:
                process_comment(value, secrets)
            except Exception:
                LOGGER.exception("コメント処理中に例外が発生しました。次のコメントを継続します")


def lambda_handler(event: Mapping[str, Any], context: Any) -> dict[str, Any]:
    """Meta Webhook の検証と Instagram コメントイベントを処理する。"""
    secrets = get_secrets()
    method = str(event.get("requestContext", {}).get("http", {}).get("method", ""))

    if method == "GET":
        query = event.get("queryStringParameters") or {}
        if (
            query.get("hub.mode") == "subscribe"
            and query.get("hub.verify_token") == secrets["verify_token"]
        ):
            return response(200, str(query.get("hub.challenge", "")))
        return response(403, "Forbidden")

    if method != "POST":
        return response(405, "Method Not Allowed")

    try:
        raw_body = get_raw_body(event)
    except (ValueError, TypeError) as exc:
        LOGGER.warning("リクエスト本文を取得できません: %s", exc)
        return response(400, "Bad Request")

    signature = get_header(event.get("headers"), "X-Hub-Signature-256")
    if not is_valid_signature(signature, raw_body, secrets["app_secret"]):
        LOGGER.warning("Webhook 署名の検証に失敗しました")
        return response(403, "Forbidden")

    try:
        payload = json.loads(raw_body)
        LOGGER.info("受信 Webhook ペイロード: %s", json.dumps(payload, ensure_ascii=False))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        LOGGER.exception("Webhook JSON の解析に失敗しました: %s", exc)
        return response(200, "OK")

    if not isinstance(payload, Mapping):
        LOGGER.warning("Webhook ペイロードがオブジェクトではありません")
        return response(200, "OK")
    process_comment_changes(payload, secrets)
    return response(200, "OK")
