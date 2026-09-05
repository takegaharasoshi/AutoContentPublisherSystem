# 2026-09-w1 リサーチ台帳(Claude WebSearch による裏取り)

Codex `--search exec` 委譲は 2026-09-03 23:40 JST に chatgpt.com バックエンドの 404 で接続不能(ログ: scratchpad/codex_research.log)のため、
本バッチは Claude 自身の WebSearch で全候補の流布例を直接確認した(スキル セクション 1 の「Claude が 1 件以上直接確認」を全問で実施)。
問題文は転載せず、類型・解法構造・流布例 URL のみ記録する。採用可否の基準: 作者不詳 + 複数の独立ドメインに流布 = folklore 級。

## 採用(朝 L1/light・7 問)

### A33 切れば切るほど公平になるもの(差し替え後)
- 類型: 言い回し(切る=シャッフル) / 答え: トランプ
- 流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13120224083 , https://peing.net/ja/q/210dfad0-9ee9-43ee-a9b2-da00267af7a9 , https://comotto.docomo.ne.jp/column/00000283-2/
- 所見: 流布形は「切っても切っても切れないもの」。別解(水・切手・縁)を封じるため「切るほど公平になる」に問い直した
- 初稿の「上は大水、下は大火事(風呂)」は 2026-09-04 レビューで「有名すぎる」により差し替え(流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11148127056 , https://okwave.jp/qa/q3503883.html )

### A34 見て言う数列(1、11、21、1211、111221 → ?)(2 回目の差し替え後)
- 類型: 法則発見(look-and-say) / 答え: 312211
- 流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1122764576 , https://japontimes.livedoor.biz/archives/54524968.html , https://www.quora.com/What-is-the-next-number-in-this-sequence-1-11-21-1211-111221-312211-13112221-2
- 所見: 国際的古典(コンウェイの数列として知られる)。答えは一意。「1〜100 に 9 は何回(20 回)」も裏取り済みで補欠に回す( https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1346484723 )
- 差し替え経緯: 初稿「1=5…5=?」→ 「逆さで 3 増える/減る数字の和(15)」は「簡単」で不採用(2026-09-04)

### A35 「日」に一画足してできる漢字
- 類型: 漢字の一画足し・列挙型 / 答え: 目・田・白・旧・旦・甲・由・申(定番 8 字)
- 流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10138380495 , https://www.okinawatimes.co.jp/articles/-/1793783
- 所見: 個数はサイトにより 8〜16(旧字・異体字の扱い)で割れる。「いくつ思いつく?」形式にして定番 8 字を答えとし、それ以上は解説で許容する

### A36 スフィンクスのなぞ(朝 4 本・昼 2 本・夜 3 本)
- 類型: 一日を一生にたとえる比喩なぞなぞ / 答え: 人間
- 流布例: https://dailyportalz.jp/kiji/Sphinx-Quiz , https://kotobank.jp/word/%E3%81%99%E3%81%B5%E3%81%84%E3%82%93%E3%81%8F%E3%81%99-3156604 , https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11263103891
- 所見: ギリシャ神話由来の世界的古典。知っている人は即答するが懐かしさでコメントを誘発できる

### A37 あるなしクイズ(語尾に「ら」)
- 類型: あるなしクイズ(法則発見) / 答え: 後ろに「ら」を付けると別の言葉になる(くじら・さくら・まくら・はしら)
- 流布例(形式): https://ja.wikipedia.org/wiki/%E3%81%82%E3%82%8B%E3%81%AA%E3%81%97%E3%82%AF%E3%82%A4%E3%82%BA , https://setuyaku-up.com/asobi-arunasi/
- 所見: 形式は作者不詳の定番。語の組み合わせは自作(自作問題)。「ない」側は「ら」を足しても語にならないことを確認(かけ→かけら、とび→とびら は語になるため「ない」側から除外)

### A38 木が 5 本
- 類型: 漢字の構成(林=2 本・森=3 本の延長) / 答え: 森林
- 流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1247541372 , https://kannbann.blogspot.com/2018/08/235.html , https://www.mokuzai-tonya.jp/geppou/2604/pdf/2604_06.pdf
- 所見: 作者不詳の定番。漢字 1 文字という思い込みを外す一手間がある

### A39 「たちつみと」
- 類型: 五十音の文字置換(A27「あいうおお=えがお」の姉妹問題) / 答え: てがみ
- 流布例: https://kabu-elife.sakura.ne.jp/inc/nazonazo/cat5/075.html , https://nihongochan.hateblo.jp/entry/2019/10/20/194611 (w5 台帳 M-15)
- 所見: 前回承認の A27 と同じ仕掛け。2 週間空くので「前回の続編」として出す

## 採用(夜 L1/deep・7 問)

### C35 3L と 5L の容器で 4L
- 類型: 容量パズル(状態遷移) / 答え: 5L→3L へ移して 2L を作り、3L を空けて 2L を入れ、5L を満たして 3L が満杯になるまで注ぐ
- 流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11103013526 , https://sairyu-sensei.com/3l5l4l/ , https://www.plies.co.jp/single-post/2017/08/28/4%E3%83%AA%E3%83%83%E3%83%88%E3%83%AB%E3%81%AE%E6%B0%B4%EF%BC%88%E7%AD%94%E3%81%88%EF%BC%89
- 所見: 国際的古典。BFS で最短手順と到達可能性を機械検証する

### C36 目隠しで硬貨を表の枚数が同じ 2 山に
- 類型: 不変量を使う手順パズル / 答え: 10 枚取り分けて全部裏返す
- 流布例: https://sist8.com/10co , https://www.soranokillingtime.com/analytical-puzzle/heads-10-coins/ , https://diamond.jp/articles/-/340346
- 所見: 作者不詳の定番。全分配パターンで一致を機械検証する

### C37 南京錠 2 つで鍵を送らずに箱を届ける
- 類型: 手順パズル(暗号技術の比喩) / 答え: 自分の錠で送る → 相手が錠を追加して返送 → 自分の錠を外して再送
- 流布例: https://gendai.media/articles/-/150729?page=2 , https://303books.jp/columns/3081/ , https://dmzcms.hyogo-c.ed.jp/takatsuka-hs/NC3/wysiwyg/file/download/26/1089
- 所見: 作者不詳の定番。「錠は何個かけてもよい」を問題文で明示する

### C38 井戸のカタツムリ(昼 3m・夜 2m・深さ 10m)
- 類型: 計算の早合点を突く古典 / 答え: 8 日目
- 流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1416591114 , https://sist8.com/30mi
- 所見: 作者不詳の国際的古典。シミュレーションで機械検証する

### C39 棒 6 本で正三角形 4 つ
- 類型: 立体への発想転換 / 答え: 三角錐(正四面体)
- 流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10102992220 , http://pzl.jp/q25 , https://sansu-seijin.jp/blog/archives/573
- 所見: 作者不詳の定番マッチ棒パズル。図なしで文章だけで成立する

### C40 曽呂利新左衛門の米粒(毎日倍)
- 類型: 倍々の直感崩し(故事) / 答え: 30 日目は 2 の 29 乗 = 約 5 億 4 千万粒
- 流布例: https://ja.wikipedia.org/wiki/%E6%9B%BD%E5%91%82%E5%88%A9%E6%96%B0%E5%B7%A6%E8%A1%9B%E9%96%80 , https://bunshun.jp/bungeishunju/articles/h1532 , https://diamond.jp/articles/-/240078
- 所見: 秀吉の御伽衆の逸話として広く流布(日数は 100 日版もある)。計算を機械検証する

### C41 暗闇の靴下
- 類型: 鳩の巣原理の古典 / 答え: 3 枚
- 流布例: https://kquoe2.hatenablog.com/entry/20090715/1254120840 , https://www.quiz-puzzle.com/question/631_q.html , https://karapaia.com/archives/52251835.html
- 所見: 作者不詳の国際的古典。全列挙で機械検証する

## 補欠(レビューで差し替えが出たら使う)

- 朝: 逆さにすると 3 増える数(6→9) https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1013500670 , https://nazoq.com/easy/Q005206.html
- 朝: 8 を半分にすると(横 0・縦 3) https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14179473489 , https://www.sakura-sha.jp/blog/sannsuu-22/ (幼稚園レベルの表記あり・軽め)
- 朝: w5 台帳の未使用候補 M-07(口+八=四)は A25(六の帽子)と同型のため保留
- 夜: ケーキを直線 3 回で 8 等分 https://nazoq.com/hard/Q030995.html , https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1468155074 (C39 と同じ「立体化」の発想なので同バッチに両方は置かない)
- 夜: ハノイの塔(3 枚 7 手)・25 頭の競走馬(7 レース)は w5 台帳 B-17 / B-10 に出典あり
- 夜: トラックがトンネルに引っかかる(タイヤの空気を抜く)は X トレンド以外に流布ページを直接確認できず保留

## 落とした候補(流布例が確認できず)

- 逆から読むと「本日」になる国(日本)・「田」の中の「口」の数・鍵があるのに開けられない(ピアノ)・口があってしゃべらない(川)・コルク栓の瓶のコイン
