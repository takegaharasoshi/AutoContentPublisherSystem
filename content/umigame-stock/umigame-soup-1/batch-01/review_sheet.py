"""batch-01 の素材レビューシート work/review.html を生成する。

実行方法: ``python3 review_sheet.py``（API キー不要）。
21-6d3 で probe_test.py から改名。旧プローブは退役（本番経路の評価は services/comment-reply/tools/probe_run.py）。
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "common"))

from stock_items import ITEMS  # noqa: E402

WORK_DIR = HERE / "work"
REVIEW_PATH = WORK_DIR / "review.html"

# review.html のスタイル（スマホ縦持ちを既定にした 1 カラム。表は使わず縦積みのカードで出す）
REVIEW_CSS = """
:root{--bg:#fff;--fg:#1b1f24;--muted:#5c6672;--line:#d8dee6;--card:#f5f7fa;
      --bad:#c0392b;--bad-bg:#fdecea;--warn:#8a6100;--warn-bg:#fff6dc;--ok:#1e7a46;--accent:#2c5aa0}
@media (prefers-color-scheme:dark){
  :root{--bg:#14171a;--fg:#e6e9ed;--muted:#9aa4b0;--line:#2c333b;--card:#1c2126;
        --bad:#ff8a7a;--bad-bg:#3a1f1c;--warn:#f0c060;--warn-bg:#37301a;--ok:#6ed49b;--accent:#8ab4f8}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);line-height:1.65;
     font:16px/1.65 -apple-system,BlinkMacSystemFont,"Hiragino Sans","Noto Sans JP",sans-serif;
     -webkit-text-size-adjust:100%}
main{padding:0 14px 64px;max-width:820px;margin:0 auto}
.bar{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);
     padding:8px 14px;max-width:820px;margin:0 auto}
.bar-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.bar-row+.bar-row{margin-top:6px}
.muted{color:var(--muted);font-size:13px}
.filters .f{font:inherit;font-size:14px;padding:7px 12px;min-height:38px;border:1px solid var(--line);
     border-radius:999px;background:var(--card);color:var(--fg);text-decoration:none;display:inline-flex;
     align-items:center;cursor:pointer}
.filters .f.on{background:var(--accent);border-color:var(--accent);color:#fff}
.note{color:var(--muted);font-size:13.5px;margin:14px 0}
h2{font-size:17px;margin:28px 0 10px;padding-bottom:6px;border-bottom:2px solid var(--line)}
.index{display:flex;flex-direction:column;gap:8px}
.idx{display:flex;align-items:center;gap:10px;padding:12px;border:1px solid var(--line);border-radius:10px;
     background:var(--card);color:inherit;text-decoration:none;min-height:52px}
.idx-no{font-weight:700;font-variant-numeric:tabular-nums}
.idx-title{flex:1;font-size:15px}
.idx.done{opacity:.5}
.item{scroll-margin-top:96px;padding-top:4px}
.item-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px;margin-top:34px}
.item-h .no{color:var(--accent)}
.tag{font-size:12px;color:var(--muted);font-weight:400}
.problem{background:var(--card);border-left:4px solid var(--accent);border-radius:0 8px 8px 0;
     padding:12px 14px;margin:10px 0;font-size:16.5px}
.len{display:block;color:var(--muted);font-size:12px;margin-top:6px}
.core{border:1px dashed var(--accent);border-radius:8px;padding:9px 12px;margin:10px 0 0;font-size:14px;
     font-weight:600;line-height:1.5}
details{margin:8px 0;border:1px solid var(--line);border-radius:8px;background:var(--card)}
summary{cursor:pointer;padding:11px 14px;font-size:14.5px;min-height:44px;display:flex;align-items:center}
details>p,details>ul{margin:0;padding:0 14px 12px}
details>ul{padding-left:32px}
details li{margin:4px 0;font-size:14.5px}
.done{display:flex;align-items:center;gap:10px;margin:16px 0 6px;padding:12px;border:1px dashed var(--line);
     border-radius:10px;font-size:15px;min-height:48px}
.done input{width:22px;height:22px}
.top{margin:6px 0 0;font-size:14px}
.handover{border-color:var(--accent)}
.handover>ul{padding:0 14px 12px 32px}
.handover li{margin:8px 0}
code{background:var(--bg);border:1px solid var(--line);border-radius:4px;padding:0 4px;font-size:13px;word-break:break-all}
a{color:var(--accent)}
details.item{margin:14px 0;background:var(--bg);border-width:1px 1px 1px 4px;border-left-color:var(--accent)}
details.item>summary{flex-wrap:wrap;gap:8px;font-size:16px;font-weight:700;padding:12px 14px;min-height:52px}
details.item>summary .no{color:var(--accent)}
details.item[open]>summary{border-bottom:1px solid var(--line)}
.item-body{padding:4px 14px 14px}
h3{font-size:15px;margin:22px 0 8px;color:var(--accent)}
.fld{margin:8px 0;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:var(--card)}
.fld .k{display:block;font-size:12.5px;color:var(--muted);margin-bottom:2px}
.fld .v{font-size:15.5px;white-space:pre-wrap;word-break:break-word}
.fld .v.mono{font:13px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace}
.fld.scene{border-color:var(--accent)}
.chat{list-style:none;margin:8px 0;padding:0}
.chat li{display:flex;gap:8px;align-items:baseline;margin:6px 0}
.chat .who{flex:0 0 auto;font-size:12px;color:var(--muted);min-width:5.5em}
.chat .say{padding:7px 11px;border-radius:12px;border:1px solid var(--line);background:var(--card);font-size:15.5px}
.chat li.master .say{border-color:var(--accent)}
.chat li.yes .say{background:var(--warn-bg);border-color:var(--warn);font-weight:700}
.chat li.gap{margin-top:12px}
details.spoiler{border-color:var(--bad)}
details.judge li .len{display:inline;margin-left:.5em}
"""

# 端末内で完結する軽い操作（確認済みチェック。localStorage は失敗しても無視する）
REVIEW_JS = """
(function(){
  var KEY='umigame-batch01-done';
  var done={};
  try{done=JSON.parse(localStorage.getItem(KEY)||'{}')||{}}catch(e){done={}}
  function save(){try{localStorage.setItem(KEY,JSON.stringify(done))}catch(e){}}
  document.querySelectorAll('input[data-done]').forEach(function(cb){
    var no=cb.getAttribute('data-done');
    cb.checked=!!done[no];
    mark(no);
    cb.addEventListener('change',function(){done[no]=cb.checked;save();mark(no)});
  });
  function mark(no){
    var link=document.querySelector('[data-idx="'+no+'"]');
    if(link){link.classList.toggle('done',!!done[no])}
  }
  function openHash(){
    var id=decodeURIComponent(location.hash.slice(1));
    var el=id&&document.getElementById(id);
    if(el&&el.tagName==='DETAILS'){el.open=true;el.scrollIntoView()}
  }
  window.addEventListener('hashchange',openHash);
  openHash();
  document.querySelectorAll('button[data-all]').forEach(function(btn){
    btn.addEventListener('click',function(){
      var open=btn.getAttribute('data-all')==='open';
      document.querySelectorAll('details.item').forEach(function(d){d.open=open});
    });
  });
})();
"""

def handover_html() -> str:
    """STATUS.md の「人間レビューへの申し送り」節を折りたたみブロックに変換する。

    スマホ 1 ページでレビューを完結させるため、review.html の先頭に埋め込む。
    節が無い場合は空文字を返す（STATUS.md 側の見出しを変えたら黙って消える）。

    Returns:
        ``<details>`` ブロックの HTML（見つからなければ空文字）。
    """
    status_path = HERE / "STATUS.md"
    if not status_path.exists():
        return ""
    lines = status_path.read_text(encoding="utf-8").splitlines()
    body: list[str] = []
    collecting = False
    for line in lines:
        if line.startswith("## "):
            if collecting:
                break
            collecting = "申し送り" in line
            continue
        if collecting:
            body.append(line)
    items = [re.sub(r"^[-*]\s+", "", ln).strip() for ln in body if ln.strip().startswith(("-", "*"))]
    if not items:
        return ""

    def inline(text: str) -> str:
        """太字とコード記法だけを HTML へ起こす（それ以外はエスケープする）。"""
        escaped = html.escape(text)
        escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
        return re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)

    return (
        "<details class='handover' open><summary>レビュー前の申し送り（STATUS.md）</summary><ul>"
        + "".join(f"<li>{inline(i)}</li>" for i in items)
        + "</ul></details>"
    )


def _field(label: str, value: str, *, count: bool = True, cls: str = "", mono: bool = False) -> str:
    """素材 1 項目をラベル付きのカードにする（字数を添える）。"""
    suffix = f"（{len(value)} 字）" if count else ""
    v_cls = "v mono" if mono else "v"
    return (
        f"<div class='fld {cls}'><span class='k'>{html.escape(label)}{suffix}</span>"
        f"<div class='{v_cls}'>{html.escape(value)}</div></div>"
    )


def material_html(it: dict) -> list[str]:
    """素材一式（版面の文言・プレイ例・セリフ・ナレーション・キャプション・プロンプト・出典）を HTML にする。

    素材の人間ゲートで全項目が目に入るようにする（2026-09-24。プレイ例がシートに無く未レビューのまま
    動画ビルドまで進んだため追加）。
    """
    out = ["<h3>版面に出る文言</h3>"]
    out.append(_field("フック（つかみ帯）", it["hook"]))
    out.append(_field("ルール帯", it["rule_text"]))
    lines = it["character_lines"]
    out.append("<div class='fld'><span class='k'>吹き出しの流れ（導入 → プレイ例 3 往復 → 締め）</span><ul class='chat'>")
    out.append(
        f"<li class='master'><span class='who'>カメロック</span>"
        f"<span class='say'>{html.escape(lines['master']['intro'])}</span></li>"
    )
    for i, line in enumerate(it["play_example"]):
        role = line["role"]
        who = "カメロック" if role == "master" else "Jr."
        yes = " yes" if role == "master" and line["text"].startswith("はい") else ""
        gap = " gap" if role == "questioner" else ""
        out.append(
            f"<li class='{role}{yes}{gap}'><span class='who'>{who}（{len(line['text'])} 字）</span>"
            f"<span class='say'>{html.escape(line['text'])}</span></li>"
        )
    out.append(
        f"<li class='master gap'><span class='who'>カメロック</span>"
        f"<span class='say'>{html.escape(lines['master']['outro'])}</span></li>"
        f"<li class='questioner'><span class='who'>Jr.</span>"
        f"<span class='say'>{html.escape(lines['jr']['outro'])}</span></li></ul>"
        "<span class='len'>黄色 = 「はい」の返答（出題者が喜ぶポーズに切り替わる）。上限は質問 16 字・返答 17 字</span></div>"
    )
    out.append("<h3>ナレーション（読み上げ用の文）</h3>")
    out.append(_field("問題文 cue", it["narration"]["problem"]))
    out.append(_field("ルール cue", it["narration"]["rule"]))
    out.append("<h3>キャプション</h3>")
    out.append(_field("投稿本文 + ハッシュタグ", it["caption"]))
    out.append("<h3>背景イラストのプロンプト</h3>")
    prompt = it["illustration_prompt"]
    scene = re.search(r"Scene:\s*(.+?)(?:\n\n|$)", prompt, re.S)
    if scene:
        out.append(_field("情景（問ごとに書いた部分）", scene.group(1).strip(), count=False, cls="scene"))
    out.append(
        "<details><summary>プロンプト全文（画風固定行・禁止事項を含む）</summary>"
        f"<p class='v mono' style='white-space:pre-wrap'>{html.escape(prompt)}</p></details>"
    )
    out.append("<h3>出典・オリジナル性メモ</h3>")
    out.append(_field("source_note", it["source_note"], count=False))
    return out


def write_review() -> None:
    """ITEMS から素材レビュー用の review.html を書き出す。"""
    out = [
        "<!doctype html><html lang='ja'><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width,initial-scale=1'>",
        "<meta name='color-scheme' content='light dark'>",
        "<title>umigame-soup-1 batch-01 素材レビュー</title>",
        f"<style>{REVIEW_CSS}</style></head><body>",
        "<header class='bar'><div class='bar-row'><b>batch-01 素材レビュー</b></div>",
        "<div class='bar-row filters'>"
        "<a class='f' href='#index'>目次</a>"
        "<button type='button' class='g f' data-all='open'>すべて開く</button>"
        "<button type='button' class='g f' data-all='close'>すべて閉じる</button></div>",
        "</header>",
        "<main>",
        "<p class='note'>各問は折りたたみ。素材 16 項目（版面の文言・プレイ例・セリフ・ナレーション・キャプション・イラストプロンプト・出典メモ）"
        "を確認した後、真相・確定事実シート・判定用の項目（コアの要点・開示文）を参照できます。各問の「確認済み」はこの端末のブラウザに保存されます。</p>",
        handover_html(),
    ]

    index_rows = []
    for it in ITEMS:
        no = it["no"]
        index_rows.append(
            f"<a class='idx' href='#{no}' data-idx='{no}'><span class='idx-no'>{no}</span>"
            f"<span class='idx-title'>{html.escape(it['title'])}</span></a>"
        )
    out.append(f"<h2 id='index'>目次（{len(ITEMS)} 問）</h2><nav class='index'>")
    out += index_rows
    out.append("</nav>")

    for it in ITEMS:
        no = it["no"]
        out.append(f"<details class='item' id='{no}' data-no='{no}'>")
        out.append(
            f"<summary><span class='no'>{no}</span> {html.escape(it['title'])}"
            f"<span class='tag'>{it['content_key']} / {it['puzzle_type']} / 難易度 {it['difficulty']}</span>"
            "</summary><div class='item-body'>"
        )
        out.append(f"<p class='core'>{html.escape(it['core'])}</p>")
        out.append(
            f"<p class='problem'>{html.escape(it['problem_text'])}"
            f"<span class='len'>{len(it['problem_text'])} 字</span></p>"
        )
        out += material_html(it)
        out.append("<h3>真相・確定事実（ネタバレ）</h3>")
        out.append(
            # truth は翌日リールのキャプションで公開する全文（21-6d3e）。書き手の改行をそのまま見せる
            f"<details class='truth spoiler'><summary>真相を見る（{len(it['truth'])} 字・翌日のキャプションで公開）</summary>"
            f"<p class='v' style='white-space:pre-wrap'>{html.escape(it['truth'])}</p></details>"
        )
        out.append("<details class='facts spoiler'><summary>確定事実シート（{}）</summary><ul>".format(len(it["fact_sheet"])))
        out += [f"<li>{html.escape(f)}</li>" for f in it["fact_sheet"]]
        out.append("</ul></details>")
        out.append(
            "<details class='judge spoiler'><summary>判定用の項目（コアの要点 {} 個・開示文）</summary>"
            "<div class='fld'><span class='k'>コアの要点 core_points（1〜3 個・1 個 20 字以内）</span><ul>".format(
                len(it["core_points"])
            )
        )
        out += [f"<li>{html.escape(p)}<span class='len'>{len(p)} 字</span></li>" for p in it["core_points"]]
        out.append("</ul></div>")
        out.append(_field("正解時の開示文 reveal_text（70 字以内）", it["reveal_text"]))
        out.append("</details>")
        out.append(f"<label class='done'><input type='checkbox' data-done='{no}'> {no} は確認済み</label>")
        out.append("<p class='top'><a href='#index'>目次へ戻る</a></p>")
        out.append("</div></details>")
    out.append("</main>")
    out.append(f"<script>{REVIEW_JS}</script>")
    out.append("</body></html>")
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_PATH.write_text("\n".join(out), encoding="utf-8")


def main() -> int:
    """素材レビューシートを生成する。"""
    write_review()
    relative_path = REVIEW_PATH.relative_to(HERE.parent.parent.parent.parent)
    print(f"review_sheet: {len(ITEMS)} 問の素材シートを {relative_path} に生成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
