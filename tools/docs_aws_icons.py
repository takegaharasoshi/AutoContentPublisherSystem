#!/usr/bin/env python3
"""設計書の図で使う AWS アイコンのパックを作る。

Phase 30-1 で新設。``docs/assets/vendor/aws-icons-<版>/svg/`` に置いた
AWS Architecture Icons の SVG（公式パッケージから使う分だけ複写したもの）を、
Mermaid の ``registerIconPacks`` が読める Iconify 形式にまとめ、
``aws-icons.js``（``window.DOCS_AWS_ICONS`` を定義する 1 ファイル）として書き出す。
``<script>`` で読むため、ファイルを直接開いた（``file://``）ときも動く。

アイコンを足すときは、公式パッケージから SVG を ``svg/`` へ複写し、
下の ``ICON_NAMES`` に図で使う名前を足してから本スクリプトを実行する。

使い方::

    python3 tools/docs_aws_icons.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PACK_DIR = REPO_ROOT / "docs" / "assets" / "vendor" / "aws-icons-07312026"
PREFIX = "aws"

# 図の中で書く名前（aws:<名前>）→ svg/ のファイル名
ICON_NAMES: dict[str, str] = {
    "aurora": "Arch_Amazon-Aurora_48.svg",
    "cloudwatch": "Arch_Amazon-CloudWatch_48.svg",
    "codebuild": "Arch_AWS-CodeBuild_48.svg",
    "codepipeline": "Arch_AWS-CodePipeline_48.svg",
    "ecr": "Arch_Amazon-Elastic-Container-Registry_48.svg",
    "ecs": "Arch_Amazon-Elastic-Container-Service_48.svg",
    "eventbridge": "Arch_Amazon-EventBridge_48.svg",
    "fargate": "Arch_AWS-Fargate_48.svg",
    "iam": "Arch_AWS-Identity-and-Access-Management_48.svg",
    "lambda": "Arch_AWS-Lambda_48.svg",
    "s3": "Arch_Amazon-Simple-Storage-Service_48.svg",
    "scheduler": "Res_Amazon-EventBridge_Scheduler_48.svg",
    "secrets-manager": "Arch_AWS-Secrets-Manager_48.svg",
    "sns": "Arch_Amazon-Simple-Notification-Service_48.svg",
    "sqs": "Arch_Amazon-Simple-Queue-Service_48.svg",
    "step-functions": "Arch_AWS-Step-Functions_48.svg",
    "vpc": "Arch_Amazon-Virtual-Private-Cloud_48.svg",
}

SVG_OPEN = re.compile(r"<svg\b[^>]*>", re.S)
VIEWBOX = re.compile(r'viewBox="0 0 ([\d.]+) ([\d.]+)"')


def to_icon(svg_text: str) -> dict[str, object]:
    """SVG 1 枚を Iconify のアイコン定義（body・幅・高さ）へ変換する。

    Args:
        svg_text: SVG ファイルの中身。

    Returns:
        ``{"body": ..., "width": ..., "height": ...}``。

    Raises:
        ValueError: ``<svg>`` 要素または ``viewBox`` が見つからない場合。
    """
    opening = SVG_OPEN.search(svg_text)
    if not opening:
        raise ValueError("<svg> 要素がない")
    box = VIEWBOX.search(opening.group(0))
    if not box:
        raise ValueError("viewBox がない")
    body = svg_text[opening.end(): svg_text.rindex("</svg>")]
    body = re.sub(r"<title>.*?</title>", "", body, flags=re.S)
    # 同じアイコンを 1 ページに複数置くと id が重複するため外す（参照する箇所はない）
    body = re.sub(r'\s+id="[^"]*"', "", body)
    body = re.sub(r">\s+<", "><", body).strip()
    return {"body": body, "width": float(box.group(1)), "height": float(box.group(2))}


def build_pack() -> dict[str, object]:
    """``ICON_NAMES`` の全アイコンを 1 つの Iconify パックにまとめる。"""
    icons = {
        name: to_icon((PACK_DIR / "svg" / filename).read_text(encoding="utf-8"))
        for name, filename in sorted(ICON_NAMES.items())
    }
    return {"prefix": PREFIX, "icons": icons}


def main() -> int:
    """パックを ``aws-icons.js`` に書き出す。"""
    pack = build_pack()
    out = PACK_DIR / "aws-icons.js"
    out.write_text(
        "/* 自動生成（tools/docs_aws_icons.py）。手で編集しない。"
        " 出典と利用条件は同じフォルダの NOTICE.md */\n"
        f"window.DOCS_AWS_ICONS = {json.dumps(pack, ensure_ascii=False, separators=(',', ':'))};\n",
        encoding="utf-8",
    )
    print(f"{out.relative_to(REPO_ROOT)}: {len(pack['icons'])} アイコン")
    return 0


if __name__ == "__main__":
    sys.exit(main())
