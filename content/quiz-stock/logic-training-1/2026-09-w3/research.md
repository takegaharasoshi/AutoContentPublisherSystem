# 2026-09-w3 リサーチ台帳(Claude WebSearch による裏取り)

w1 と同じく Claude 自身の WebSearch で全候補の流布例を直接確認した(スキル セクション 1 の「Claude が 1 件以上直接確認」を全問で実施。
Codex `--search exec` は w1 で接続不能だったため今回は使っていない)。問題文は転載せず、類型・解法構造・流布例 URL のみ記録する。
採用可否の基準: 作者不詳 + 複数の独立ドメインに流布 = folklore 級。加えて w1 レビューで確立した「答えを聞いた人が 3 秒で納得する型は朝でも不採用」
「夜は数値答え・雑学着地を避ける」を執筆前の選別に使った。

## 採用(朝 L1/light・7 問)

### A40 5+5+5=550 に線を 1 本
- 類型: 式の視覚パズル / 答え: 左の「+」に斜線 → 545+5=550(「=」→「≠」の別解も正解に取り込む)
- 流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1034575295 , https://ddnavi.com/article/d532020/a/ , https://quiz.community.fmworld.net/nazonazo/content/63/answer3.html , https://nazoq.com/hardest/Q003458.html , https://quizmondai.com/sequence-quiz-02/
- 所見: 国内で広く流布(「有名すぎる」判定のリスクは A33 風呂・A36 スフィンクスほどではないが申告する)。別解「≠」は潰さず answer に併記

### A41 8 を 8 個で 1000
- 類型: 数字パズル / 答え: 888+88+8+8+8(足し算限定では一意。verify_logic.py で全列挙)
- 流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1298194207 , https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q13314261373 , https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10245770900 , https://themathmompuzzles.blogspot.com/2011/04/eight-eights-that-are-thousand.html
- 所見: 四則を許すと別解が多数あるため「足し算だけ」と条件で閉じた。一の位を 0 にするには 8 が 5 個要る、が解説の筋

### A42 計算マジック「必ず 5」(2 回目の差し替え後)
- 類型: 計算マジック(思い浮かべた数が途中で消える) / 答え: 必ず 5(verify_logic.py で整数 −1000〜1000 と分数で確認)
- 流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1417987009 , https://land.toss-online.com/lesson/kttB1ZHLIXoLyTIwlDrj , https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1116589591 (必ず 3 になる同型)
- 所見: 作者不詳の定番の数当てマジック。視聴者が頭の中で実演でき「全員 5 になる」驚きでコメントを誘う狙い
- 差し替え経緯(2026-09-20 レビュー): 初稿「止まった時計と 1 日 1 分遅れる時計」は**簡単すぎる**で却下
  (流布例: https://blog.goo.ne.jp/lemon-stoism/e/381964bfad6d0f3418f4e579663743ea , https://kzr-2.hatenadiary.org/entry/20090714/p2 , https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1322931153 )。
  2 案目「100 チームのトーナメントは何試合(99)」は**面白くない**で却下(流布例: https://gendai.media/articles/-/103584?page=4 , https://diamond.jp/articles/-/342760 , https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1236109617 )。
  ほかに裏取り済みだった「3 時 15 分の長針と短針の角度(7.5 度)」は A44 の差し替えに使った

### A43 時計の文字盤を直線 2 本で 3 分割
- 類型: 文字盤の分割(法則発見) / 答え: {11,12,1,2}{3,4,9,10}{5,6,7,8}(各 26)。verify_logic.py で「交わらない 2 本」の分け方が一意であることを全列挙
- 流布例: https://nrich.maths.org/problems/split-clock-face , https://www.quora.com/How-do-I-draw-2-straight-lines-on-a-clock-face-to-separate-it-into-3-parts-and-that-each-parts-numbers-add-up-to-26 , https://puzzleaday.wordpress.com/2019/02/06/dividing-a-clock-face-into-sections/ , https://note.com/todoroki18/n/n04acaa7fc644 (割れた文字盤の破片の和が等しい、の同型)
- 所見: 日本語の流布例は同型(破片)が 1 件で、英語圏の流布が主。folklore 級と判断

### A44 指の頭文字「お・ひ・□・く・こ」(2 回目の差し替え後)
- 類型: 法則発見(頭文字) / 答え: な(親指・人差し指・中指・薬指・小指。verify_logic.py で頭文字列を確認)
- 流布例: https://nazoq.com/hard/Q002762.html , https://www.nazo2.net/jyoukyuu/062.html
- 所見: 作者不詳の定番。数字でも五十音でもない「身体の名前」に気づく型で、朝の帯(なぞなぞ・言葉あそび)に合う。イラストはカード 5 枚の文字を描かせる提示物
- 差し替え経緯(2026-09-20 レビュー): 初稿「一〜十の漢数字で画数最多は四(自作問題)」は**簡単**で却下。2 案目「3 時 15 分の長針と短針の角度(7.5 度)」は**数学っぽい**で却下
  (流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1367066288 , https://jp.quora.com/tokei-ga-3-toki-15-fun-wo-sashi-te-iru-toki-choushin-to-tanshin-no-kan-no-kakudo-ha , https://okwave.jp/qa/q7127107.html )。
  同型の候補「ひ・ふ・み・よ・い・む・な・や・こ・□ = と(和語の数え方)」( https://jpnculture.net/hifumiyo/ , https://ameblo.jp/k-konnothalasso/entry-12237013656.html )は補欠へ

### A45 母音送り「柿→菊、雨→芋、蟹→絹、馬→?」(5 回目の差し替え後・承認)
- 類型: 法則発見(読みの各文字の母音を 1 段送る。あ→い→う→え→お) / 答え: えみ(笑み)
- 出典: 自作問題(形式のみ定番。A32 と同じ対応当て)。verify_logic.py で 4 組すべてが母音送りの関係であること、および逆順・循環並べ替えでは説明できないことを機械確認
- 所見: 操作は「漢字 → 読み」「母音を 1 段送る」の 2 段で、2 段目が非自明。**朝の最難問**として位置づけ、リスト順は朝の最後に置く
- 差し替え経緯(2026-09-20 レビュー・4 回差し替え): ①「本棚の虫(24cm)」= 面白くないひっかけ ②「マラソンの順位(2 位)」= 面白くない
  ③「鏡に映せない自分の顔(寝顔)」= 簡単(流布例: https://nazo-nazo.net/level1/633/ , https://nazonazonavi.net/mondai/00/008803.htm , https://nazoq.com/normal/Q031788.html )
  ④「濁点の法則(天気→電気)」= 簡単 ⑤「循環並べ替え(時計→毛糸)」= 簡単
- **却下 9 件から見えた帯(朝スロット)**: 答えが数値の問題は「面白くない」、1〜2 段でも操作が素直なものは「簡単」。通るのは A32 級の非自明な操作か、参加型の驚き

### A46 地球にロープ
- 類型: 規模感の直感外し / 答え: 約 16cm(1/(2π) m。地球の大きさに依存しない。verify_logic.py で半径 6371km と 1m の両方で確認)
- 流布例: https://plaza.rakuten.co.jp/umidas21/diary/200612240000/ , https://hama-1987.cocolog-nifty.com/blog/2013/07/post-a49b.html , https://www.omoshiro-suugaku.com/entry/sekidounirope , https://nazesuugaku.com/rope_surrounds_earth/ , https://gendai.media/articles/-/106285?page=3
- 所見: 答えが数値だが「答えを聞いても納得できない距離」が最も大きい古典(A38 級)

## 採用(夜 L1/deep・7 問)

### C42 のろのろ馬レース
- 類型: 水平思考(一言で膠着を解く) / 答え: 「馬を交換しろ」
- 流布例: https://diamond.jp/articles/-/341503 , https://www.oricon.co.jp/article/2556546/ , https://sist8.com/2horse , https://diamond.jp/articles/-/369942
- 所見: 作者不詳の古典。「後にゴールした馬の持ち主の勝ち」と「馬の持ち主」を明示して交換の一言が効くようにした

### C43 ロウソク問題
- 類型: 道具の機能的固着を外す / 答え: 画びょうの箱を壁に留めて台にする
- 流布例: https://ja.wikipedia.org/wiki/%E3%83%AD%E3%82%A6%E3%82%BD%E3%82%AF%E5%95%8F%E9%A1%8C , https://www.weblio.jp/content/%E3%83%AD%E3%82%A6%E3%82%BD%E3%82%AF%E5%95%8F%E9%A1%8C , https://mitani3.com/blog/2010/07/post-223.html , https://note.com/llc100/n/n67d70eb084d9
- 所見: 1945 年ドゥンカーの心理学実験に由来するが、作者を離れて古典として流布(TED 講演で広く知られる)。「箱に入った画びょう」を問題文で明示することが成立条件

### C44 一休の水あめ
- 類型: とんち(一休咄) / 答え: 茶碗を割り「お詫びに毒を食べて死のうとした」
- 流布例: http://hukumusume.com/douwa/amime/jap/j03_19.html , https://news.mynavi.jp/article/20220928-2465292/ , https://tap-biz.jp/lifestyle/trivia/1038435?page=2 , https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1011556050
- 所見: 江戸期の一休咄。「毒」「死ぬ」の語はとんちの構造上外せない(和尚の嘘を逆手に取る)ため残した(プラットフォーム配慮の申告対象)

### C45 曹沖のゾウ(曹沖称象)
- 類型: 故事(等価置換の手順) / 答え: 船の喫水線に印 → 同じ沈みまで石を積む → 石を量る
- 流布例: https://ja.wikipedia.org/wiki/%E6%9B%B9%E6%B2%96 , https://hajimete-sangokushi.com/2015/01/25/post-1231/ , https://history-ancient.com/soucyuu-sangokusi/ , https://baike.baidu.com/item/%E6%9B%B9%E5%86%B2%E7%A7%B0%E8%B1%A1/5085
- 所見: 『三国志』魏書由来の逸話。前バッチ C41(アルキメデスの王冠)と「水を使う」点が近いので夜の中盤に置き、レビューで申告する

### C46 残ったリンゴ(かごごと)
- 類型: 水平思考(言葉の隙間) / 答え: 最後の 1 人はかごごと受け取った
- 流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1431927394 , https://ameblo.jp/01180622/entry-10290556264.html , https://mixi.jp/view_bbs.pl?comm_id=4284716&id=43356568
- 所見: 作者不詳の定番。「切ったり分けたりはしていない」で別解(6 等分など)を閉じた

### C47 橋の番人
- 類型: 水平思考(ルールをそのまま利用する逆転) / 答え: 5 分弱で向きを変え、番人に目的の岸へ追い返してもらう
- 流布例: http://sui-hei.net/mondai/show/5849 , https://www.quiz-puzzle.com/question/74_q.html , https://www.quora.com/If-a-bridge-which-takes-30-mins-to-cross-has-a-guard-situated-in-house-half-way-along-the-bridge-who-checks-every-15mins-to-catch-people-crossing-and-if-caught-he-sends-them-back-the-way-they-came-how-can-you-get
- 所見: 国内(ラテシン・IQ クイズ)と英語圏(30 分/15 分版)に流布。「番人と話さず、誰も傷つけずに」で力づく・買収の別解を閉じた

### C48 ケーキを 3 回で 8 等分
- 類型: 立体への発想転換 / 答え: 上から十字に 2 回 + 横から水平に 1 回(verify_logic.py でモンテカルロ体積が等しいことを確認)
- 流布例: https://nazoq.com/hard/Q030995.html , https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1468155074 , https://www.torito.jp/puzzles/308.shtml , https://smart-flash.jp/lifemoney/158343/
- 所見: w1 台帳の補欠(C39 棒 6 本と同じ「立体化」のため同バッチには置かない、としていた。バッチが変わったので採用)。「動かしたり重ねたりしてはいけない」で積み重ね解を閉じた

## 補欠(レビューで差し替えが出たら使う)

- 朝: 池のハスの葉(毎日 2 倍・30 日で全面 → 半分は 29 日目)。流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10140752310 , https://note.com/numa_fpt/n/n8afcaf3485f4 , https://blog.hamachiya.jp/entry/20091106/exp 。**答えを聞いて 3 秒で納得する型**のため本採用から外した
- 朝: 本棚の虫(洋書 10 巻・24cm。A45 初稿。面白くないひっかけで却下)
- 朝: マラソンの順位(2 位。A45 2 案目。面白くないで却下)
- 朝: 鏡に映せない自分の顔 = 寝顔(A45 3 案目。簡単で却下)
- 朝: 濁点の法則(柿→鍵・蓋→豚・戸→土 → 天気→電気。A45 4 案目。簡単で却下。自作)
- 朝: 循環並べ替え(猫→こね・犬→ぬい・蜜柑→かんみ → 時計→けいと。A45 5 案目。簡単で却下。自作)
- 朝: 錨(使うときに捨て、使わないときはしまう)。流布例: https://www.1101.com/nazonazo/021025_kaitou.html 。別解(網・釣り針)が塞ぎにくく保留
- 朝: 秘密(2 人なら守れるが 3 人だと守れない)。日本語の流布ページを直接確認できず保留
- 朝: ひ・ふ・み・よ・い・む・な・や・こ・□ = と(和語の数え方の頭文字。A44 と同型)。流布例は上の A44 の差し替え経緯に記載
- 朝: 3 時 15 分の長針と短針の角度(7.5 度)。数学っぽいで却下(A44 2 案目)
- 朝: 一〜十の漢数字で画数最多は四(自作問題・A44 初稿。簡単で却下)
- 朝: 積んだサイコロ 3 個の見えない面の合計(向かい合う面の和 7 を使う)。流布例: https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14225803194 , https://www.chugakujuken.com/sansu/kaisei-tsukukoma-nada/11_saikoro/ 。算数色が強め
- 朝: 鏡に映った時計(3 時 20 分に見えたら実際は 8 時 40 分)。流布例: https://houkago.gakken.jp/contents/M20060.html , https://www.koov.io/column/14990 , https://kyozai-okiba.com/1_83.html 。時計ものが 3 問になるため外した
- 朝: 取れば取るほど大きくなるもの(穴)。流布例: https://www.rarejob.com/englishlab/column/20170306/ , https://nazoq.com/hard/Q000585.html 。逆説型・軽め
- 朝: 小町算(1〜9 の間に + − で 100。例 123−45−67+89)。流布例: https://ja.wikipedia.org/wiki/%E5%B0%8F%E7%94%BA%E7%AE%97 , https://www.weblio.jp/content/%E5%B0%8F%E7%94%BA%E7%AE%97 。A41 と型が重なるため外した
- 朝: w1 台帳の補欠(逆さで 3 増える 6→9 / 8 を半分で 0・3)も残っている
- 夜: メイヤーの 2 本のひも(ペンチを重りにして振り子)。流布例: https://www.jstage.jst.go.jp/article/jjsai/18/3/18_275/_pdf , http://www.ri.aoyama.ac.jp/~susan/komaba/insight1.pdf , https://knowledge-bridge.info/science/creativity/2435/ 。C43 と同じ機能的固着型のため同バッチに 2 つ置かなかった
- 夜: タレスのピラミッド(自分の影が身長と同じ長さになる時刻に影を測る)。流布例: https://ja.wikipedia.org/wiki/%E3%82%BF%E3%83%AC%E3%82%B9 , https://www.eikoh-link-study.com/kono220728/ , https://mathsuke.jp/thales/ 。C45 と同じ「測る故事」のため補欠

## 落とした候補

- 4 隅の猫(各猫の前に 3 匹 → 4 匹)・倒れた道標・深い穴のピンポン玉(水を注ぐ)・樽がちょうど半分か(傾けて底の縁): いずれも流布ページを直接確認できず
- トラックがトンネルに引っかかる: X トレンド + 実例記事( https://togetter.com/li/2731998 )はあるが「荷を降ろす / 空気を抜く」で答えが割れるため不採用
- 4 人で 4 分で 4 個 → 100 人で 100 個は 4 分: 気づき一発型(簡単)
