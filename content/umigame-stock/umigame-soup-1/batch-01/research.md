# batch-01 リサーチ台帳（Codex Web リサーチ + note 記事の作問法）

2026-09-04 実施。`codex --search exec`（gpt-5.6-terra・read-only・stdin を `< /dev/null` で閉じる）に委譲し、
ウミガメのスープ / situation puzzle の「題材（モチーフ）とコアの仕掛け」を 30 件収集した（プロンプトと生出力は scratchpad。問題文は転載していない）。
本家「ウミガメのスープ」は除外。**この台帳は着想の型を確認するためのもので、採用 10 問はいずれも既存問題の転載・改変ではない**（各問の `source_note` に型・モチーフ・作問過程を記録）。

## 作問法（note 記事 https://note.com/suekai0217/n/n35128e606a9b の要点。変えずに守るポイント）

- 基本の 4 ステップ: ① モチーフを決める → ② 連想する → ③ 言い方を変える（具体化 / 抽象化。ここで「コア = 引っかけるポイント」が決まる）→ ④ 不思議にする（ミスリード先の常識を洗い出し、その逆を付与する）
- 良い問題の 3 条件: ① 答えのコアがハッキリしている ② 動線（問題文の取っ掛かりから正解までの最短ルート）が説明できる ③ 現実離れしていない（架空設定・マニアック知識を避ける。小中学校の知識なら可）
- 原理: わからないストレスをカタルシスに変換する「納得感」を最優先する
- 2 類型: 物語復元型（A→B→C の物語から B を抜いて A→C を出す = 最も有効な切り出し）/ 意味誤誘導型（語の多義性・常識の逆。4 ステップはこの型向け）
- 記事の結び「水平思考のゲームにロジカルなメソッドは存在しない。自由に作る」

## オリジナル性の基準（21-4a で決定。セット別設計書セクション 4 #13 に反映）

- 既存問題の問題文・真相を転載しない。語句・登場人物・舞台の置き換えだけの改変もしない
- 借りてよいのは「型（物語復元 / 意味誤誘導）」と「仕掛けの構造」（例: 遠回りが目的達成 / 動詞の多義性 / 見えない合図）まで。モチーフ・真相・問題文は新規に作る
- 台帳で `fame: classic` の題材（雨の日のエレベーター・雪だるまの残骸・ホーム = 本塁 等）は、構造ごと避ける（知っている人が即答してしまい、非オリジナルにも見えるため）
- `source_note` に「完全オリジナル」宣言 + 型 + モチーフ → 連想 → 逆にした常識 を書く（validate.py が宣言の有無を検査）

## 採用 10 問と着想の型

| No | 題名 | 型 | 借りた構造（台帳の該当行） | 新規のモチーフ・真相 |
|---|---|---|---|---|
| U01 | 毎月同じ本を借りる老人 | story | なし（4 ステップで新規） | 図書館 / 貸出カードに残る妻の名前 |
| U02 | 反対方向の電車に乗る男 | story | 遠回りが目的達成（#10 の構造のみ） | 通勤電車 / 始発駅で座る |
| U03 | 毎晩 9 時の小石 | story | 見えない合図（#09 の構造のみ） | 小石 / 無事の合図 |
| U04 | 曲が鳴ると走り出す町 | story | 音の実用的役割（#09 の構造のみ） | 商店の曲 / バス 5 分前の合図 |
| U05 | 割れた皿と焦げた鍋 | story | なし（4 ステップで新規） | 台所の失敗 / 母の誕生日 |
| U06 | 妻に打たれたものを食べる男 | misdirection | 作業と事件の両方に使える動詞（#23 の構造のみ） | 打つ = 手打ちうどん |
| U07 | 30 人全員を落とした先生 | misdirection | なし（4 ステップで新規） | 落とす = 体重 |
| U08 | 毎朝みんなを泣かせる男 | misdirection | なし（4 ステップで新規） | 泣かせる = 玉ねぎ |
| U09 | 負けるほど給料が上がる | misdirection | なし（常識の逆） | ヒーローショーの悪役 |
| U10 | 電車が一本も来ない駅 | misdirection | 建物以外にも成立する場所語（#30 の構造のみ） | 駅 = 道の駅 |

## Codex 収集分（30 件。着想の型の確認用。問題文は転載していない）

| # | モチーフ | 型 | 有名度 | 日常 | コア | 転用メモ | 確認 URL |
|---|---|---|---|---|---|---|---|
| 01 | 雨の日のエレベーター | story | classic | ○ | 住人が途中階で降りるのを好みだと誤認させる。実際は背が低く、雨の日だけ傘を使って高い階のボタンを押せる。 | 届かない物を、雨具・棒・子どもの肩車など一時的な補助手段に置換する。 | https://puzzlewocky.com/brain-teasers/situation-puzzles/ https://www.autoenglish.org/games/SituationPuzzles.pdf |
| 02 | 庭に残ったニンジンと石炭 | story | classic | ○ | 誰かが散らかした物に見えるが、かつて一体だった雪だるまが溶けた残りである。現在の物体だけでなく、直前の形を復元させる仕掛け。 | 工作・誕生日飾り・砂の城など、完成物が消えて部品だけ残る題材にする。 | https://trainthinking.com/lateral-thinking-puzzles/ https://icebreakerideas.com/lateral-thinking-puzzles/ |
| 03 | 無銭で店を出る買い物客 | story | known | ○ | 万引きに見える行動を、従業員がゴミを運び出す業務だと反転させる。買い物かごの用途と人物の立場が伏せられている。 | レジを通らない持ち出しを、返品・配送・清掃・撮影準備など正当な仕事に置き換える。 | https://icebreakerideas.com/lateral-thinking-puzzles/ |
| 04 | 虎へ走る女性 | story | known | ○ | 野生の虎に近づく危険行為に見えるが、女性は動物園の来園者であり、安全な環境だと分かる。場所の前提を反転する。 | 危険な対象を、水族館・画面・着ぐるみ・展示品など安全な隔たりのあるものに変える。 | https://icebreakerideas.com/lateral-thinking-puzzles/ |
| 05 | 金属の筒の中で震える女性 | story | known | ○ | 閉じ込められたように見えるが、正体は飛行機内であり、恐怖の原因は飛行そのもの。場所を抽象語で提示して誤認を誘う。 | エレベーター、MRI、洗車機、観覧車などを外形だけで表現して場所を伏せる。 | https://icebreakerideas.com/lateral-thinking-puzzles/ |
| 06 | 父親がゲーム機をハンマーで解決 | story | obscure | ○ | ゲーム機を壊したと受け取らせるが、実際には高い棚を取り付けて子どもだけ届かなくした。破壊行為と工具使用を混同させる。 | ハンマー以外にも、脚立・鍵・タイマーなどの道具を「禁止のため」と誤認させる。 | https://icebreakerideas.com/lateral-thinking-puzzles/ |
| 07 | 大規模な車の玉突き事故 | story | known | ○ | 多数の車両と消防車が絡む事故に見えるが、全て子どもが遊ぶ玩具である。規模感と実物性を反転させる。 | 工事現場・街・災害現場を、ジオラマ、ゲーム画面、写真の接写へ転用する。 | https://icebreakerideas.com/lateral-thinking-puzzles/ |
| 08 | 水を頼んだ客と拳銃の店主 | story | classic | ○ | 脅迫された客が感謝する矛盾を、しゃっくりを驚かせて止める善意の対応で解く。注文した水は本当の目的ではない。 | 苦痛を止めるための意外な驚かせ方を、くしゃみ・眠気・緊張などに置き換える。 | https://trainthinking.com/lateral-thinking-puzzles/ https://www.autoenglish.org/games/SituationPuzzles.pdf |
| 09 | 音楽が止まって困る曲芸師 | story | known | × | 演出用に思える音楽が、目隠し状態の曲芸師にとって位置を測る合図だったと判明する。BGMの実用的な役割を隠す。 | チャイム、香り、振動、店内放送を、人物の行動を支える見えない目印にする。 | https://trainthinking.com/lateral-thinking-puzzles/ |
| 10 | 通行を制限する橋の兵士 | story | obscure | ○ | 目的地へ向かう者が正面突破を試みると誤認させる。一度反対方向へ歩いてから戻り、外から来た人に見せることで通過する。 | 一方通行、入場口、順番待ちなど、ルールが観察される向きだけを利用する構造へ変える。 | https://criticalthinkingsecrets.com/top-5-lateral-thinking-puzzles-tips-and-answers-included/ |
| 11 | 消灯したまま向かい合う黒い車 | story | known | ○ | 夜間だと思わせる条件が並ぶが、実は雲で太陽が見えない昼間である。星や月が見えないことを暗闇の証拠だと誤認させる。 | 「明かりがない」を、日中・停電後の窓際・スクリーン投影など別の光源で反転させる。 | https://puzzlewocky.com/brain-teasers/situation-puzzles/ |
| 12 | 家に入れない帰宅者 | story | obscure | ○ | 自宅を間違えたように見えるが、酔っていた本人から友人が鍵を預かっていたため入れない。正しい場所でも必要物を欠く構造。 | 鍵の代わりにスマホ、社員証、暗証番号、眼鏡などを欠けさせる。 | https://icebreakerideas.com/lateral-thinking-puzzles/ |
| 13 | 高層ビルから飛び降りて無傷の人 | story | known | ○ | 住んでいる建物の高さと、飛び降りた窓の高さを同一視させる。実際に使ったのは低層階の窓である。 | 「住んでいる階」と「行動した階」を分け、階段・非常口・ベランダなどに変える。 | https://icebreakerideas.com/lateral-thinking-puzzles/ |
| 14 | 地下室を開けてはいけない少女 | story | known | × | 地下室に危険があると見せるが、少女自身が地下室で暮らしており、扉の向こうは外の世界である。禁止対象の位置関係を反転する。 | 倉庫、舞台裏、ペット用スペースなどで「中にいる側」からの禁止に置き換える。 | https://puzzlewocky.com/brain-teasers/situation-puzzles/ |
| 15 | 給与を秘密にした平均計算 | story | obscure | ○ | 平均を出すには全員が給与を公開する必要があると思わせる。最初の人が乱数を足して順に合計し、最後にその数を引けば秘密を保てる。 | 点数、歩数、寄付額など、個人情報を伏せたまま集計する題材にする。 | https://criticalthinkingsecrets.com/top-5-lateral-thinking-puzzles-tips-and-answers-included/ |
| 16 | ホームへ走る人と仮面の男 | misdirection | classic | ○ | 自宅へ逃げる犯罪場面に見せるが、「ホーム」は野球の本塁で、仮面の男は捕手である。日常語を競技用語として反転する。 | 駅のホーム、ゴール、アウト、セーブなど、日常語と競技用語が重なる語を使う。 | https://puzzlewocky.com/brain-teasers/situation-puzzles/ https://trainthinking.com/lateral-thinking-puzzles/ |
| 17 | ホテル前まで車を押す破産者 | misdirection | classic | ○ | 車とホテルを現実の交通・宿泊だと解釈させるが、正体はボードゲームの駒とマスである。物語の縮尺を盤上へ反転する。 | 人生ゲーム、カードゲーム、アプリゲームなどの用語を現実描写のように使う。 | https://puzzlewocky.com/brain-teasers/situation-puzzles/ https://www.autoenglish.org/games/SituationPuzzles.pdf |
| 18 | 塔を跳び越える馬 | misdirection | known | ○ | 動物と建物の事故に見えるが、馬はチェスのナイト、塔はルーク、消えた人は取られた駒である。実体物の語をゲーム上の駒へ反転する。 | 将棋、トランプ、スマホゲームの駒や役を、現実の人物・物体として描写する。 | https://trainthinking.com/lateral-thinking-puzzles/ |
| 19 | 金曜日に町へ来て金曜日に去る旅人 | misdirection | classic | ○ | 曜日の経過が矛盾するように見えるが、「金曜日」は乗っている馬の名前である。時間語を固有名詞として反転する。 | 曜日・月・色・数字を、ペット名、店名、乗り物名に転用する。 | https://trainthinking.com/lateral-thinking-puzzles/ https://www.autoenglish.org/games/SituationPuzzles.pdf |
| 20 | 何度もひげを剃るのにひげがある男性 | misdirection | known | ○ | 自分のひげを剃る動作だと決めつけるが、男性は理容師で客のひげを剃っている。動作の対象を反転する。 | 洗う、撮る、教える、運ぶなど、職業上は他人に行う動詞で組み立てる。 | https://trainthinking.com/lateral-thinking-puzzles/ |
| 21 | 同時刻生まれなのに双子でない兄弟 | misdirection | classic | ○ | 二人しか生まれなかったと補完してしまうが、実際には三つ子以上の一部である。人数の省略を利用する。 | 二人の比較に見せて、第三者・第三の物・追加の順番を隠す。 | https://icebreakerideas.com/lateral-thinking-puzzles/ https://www.autoenglish.org/games/SituationPuzzles.pdf |
| 22 | 息子を診られない外科医 | misdirection | classic | ○ | 外科医を男性、父親を唯一の親と無意識に決めつける。外科医は患者の母親であり、論理的矛盾は存在しない。 | 職業・家族役割・年齢への固定観念を、現代的な人物設定で一つだけ外す。 | https://puzzlewocky.com/brain-teasers/situation-puzzles/ https://criticalthinkingsecrets.com/top-5-lateral-thinking-puzzles-tips-and-answers-included/ |
| 23 | 夫を撃って水に沈めた妻 | misdirection | known | ○ | 暴力事件の動詞に見せるが、「撃つ」はカメラ撮影、「水に沈める」は写真の現像である。連続した動詞の別義を重ねる。 | 切る、焼く、捕まえる、落とすなど、作業と事件の両方に使える動詞を連結する。 | https://criticalthinkingsecrets.com/top-5-lateral-thinking-puzzles-tips-and-answers-included/ |
| 24 | 栓を抜かずに瓶から硬貨を出す | misdirection | known | ○ | 栓を外へ抜くことだけが「抜く」だと思わせる。栓を瓶の中へ押し込めば、硬貨は取り出せる。 | 禁止された動作の反対方向や、禁止文に含まれない手段を探す制約型にする。 | https://criticalthinkingsecrets.com/top-5-lateral-thinking-puzzles-tips-and-answers-included/ |
| 25 | 半分入った樽 | misdirection | known | ○ | 計量器か計算が必要だと思わせるが、樽を傾けて水面と底の見え方を観察すれば判定できる。数値問題を視覚的な操作へ反転する。 | 容器、影、反射、重心などを使い、道具なしの観察で判定させる。 | https://criticalthinkingsecrets.com/top-5-lateral-thinking-puzzles-tips-and-answers-included/ |
| 26 | バス運転手の目の色 | misdirection | known | ○ | 乗客数の計算に注意を奪われるが、問題の主語である「あなた」が運転手である。外部情報ではなく聞き手自身に答えがある。 | 読者・視聴者・出題者が文中の役を担っている二人称トリックにする。 | https://icebreakerideas.com/lateral-thinking-puzzles/ |
| 27 | 丸いマンホールのふた | misdirection | classic | ○ | 製造上の都合を考えさせるが、丸いふたは向きを変えても穴の中へ落ちない。形状の意外に単純な物理性が答えになる。 | コップのふた、排水口、郵便受けなど、形が安全性を決める身近な物へ変える。 | https://www.autoenglish.org/games/SituationPuzzles.pdf |
| 28 | アダムとイブを見分ける人物 | misdirection | known | × | 顔を知っていたから判別したように見えるが、へそがないという創世神話上の特徴で見分ける。人物認識を固有の身体的手掛かりへ反転する。 | 架空設定を避けるなら、制服の名札、日焼け跡、手袋の跡などで初対面の人物を特定させる。 | https://icebreakerideas.com/lateral-thinking-puzzles/ https://www.autoenglish.org/games/SituationPuzzles.pdf |
| 29 | 亡くなった兄を持つ盲人 | misdirection | known | ○ | 「兄弟」という語から男性だと補完してしまうが、盲人は亡くなった男性の姉妹である。性別を明記しない親族語を利用する。 | いとこ、子、親、きょうだいなど、性別や年齢を限定しない親族語で固定観念を外す。 | https://www.autoenglish.org/games/SituationPuzzles.pdf |
| 30 | 山中の「キャビン」 | misdirection | classic | × | 山小屋を意味すると決めつけるが、キャビンは墜落した飛行機の客室である。場所を示す語の多義性で場面を反転する。 | 客室、ホーム、席、教室など、建物以外にも成立する場所語を使う。 | https://puzzlewocky.com/brain-teasers/situation-puzzles/ https://trainthinking.com/lateral-thinking-puzzles/ |

所見: 収集分は英語圏の situation puzzle の定番が多く（日本語サイトの個別投稿は検索で拾えなかった）、日本語の作問には「構造だけ借りて日本の日常へ置き換える」使い方になる。
半数以上を「誰も死なない・日常の不思議」系にする指示は守られた。採用 10 問は死者・事件を含まない（U03 は転倒のみ）。
