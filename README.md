# teamD

## 動かし方
    ・ config.pyファイルを「teamD / config.py」に配置する。(データベースを作り直す場合のみ)
    ・ app.pyを実行しブラウザで表示させるとindex.htmlが表示される。

    ※Dockerの設定はまだなのでflask,requestsなどのインストールが必要


## ファイル説明
    フロントエンド
    ・templates / index.html : データベースからID,Name,imageを表示させる

    バックエンド
    ・app.py
    データベースに接続し、htmlファイルにデータを渡す。実行すると、URLがタ ーミナルに表示されるのでブラウザで開くと、コンテンツが表示される。

    ・database.py
    データベースの表示や保存など基本操作の関数が入っている。実行するとsweets.dbが作成される。
    ※すでにsweets.dbが存在している状態で実行するとうまくいかないため、sweets.dbを消してから実行してください。

    -----------------------------------
    以下のファイルは実行しない
    ・sweets.db : データベース
    ・sweets_api.py : お菓子の虜APIを動かす。
    ・instagram_api.py : Instagram APIを動かす。    

    ・config.py
    instagram APIを使用するためのビジネスIDとアクセストークンの情報が入っている。
    ※git hub上に公開することはセキュリティ上の問題があるため各自でteamDディレクトリの配下に置いてください。 

## データベースから情報を取得する方法

### Instagramデータベース
    配列'instagram'にいいね数が多い順に投稿データが格納されている。(4位以下はニュースに使う？)

    instagram[0] ← 1位
    instagram[1] ← 2位
    instagram[2] ← 3位
    ...

    instagram[n].〇〇で投稿データにアクセスできる
    ※ n=0,1,2,3,...

|  instagram.〇〇  | 意味 |
| ---- | ---- |
|id | ID |
|like | いいね数 |
|comment | コメント数 |
|follower| フォロワー数 |
|post| 投稿数 |
|text| 投稿文|
|image| 画像 |
|username| 名前 |
|link| Instagramの投稿リンク |
|date| 投稿日時 |

### お菓子の虜データベース
    配列'snack', 'chocolate', 'cookie', 'candy', 'japanese', 'limited'にそれぞれ最新順にデータが格納されている。

    snack[0] ← 最新のスナック菓子
    snack[1]  
    snack[2]  
    ...

    snack[n].〇〇で投稿データにアクセスできる
    ※n=0,1,2,3,...,29(それぞれ最新データ30個登録してます！)




|  snack.〇〇  | 意味 |
| ---- | ---- |
|id | ID |
|name | 商品名 |
|kana | ふりがな ※1 |
|maker | メーカー |
|price | 値段 |
|type | 種類 |
|data | 登録日 ※2 |
|url | 商品紹介ページのURL |
|tags | タグ |
|image | 画像のURL |
|comment | 投稿文 |

※1 kanaは結構欠損が多かったので使わない方向で<br>
※2 登録日であって、発売日ではないから不要<br>

### HTMLでの書き方
    以上で述べた変数を{{}}でくくって使用する。
    例
    {{snack[0].image}} ← スナック菓子の画像
    {{chocolate[1].name}} ← チョコの名前

## データベースの構成
sweets.dbには以下の7つのテーブルがある。<br>
Snack : スナック<br>
Chocolate : チョコレート<br>
Cookie : クッキー<br>
Candy : 飴・ガム<br>
Rice_cracker : せんべい・和風<br>
Limited_sweets : 限定品<br>
Instagram : インスタの投稿<br>
OrderedInstagram : Instagramテーブルをいいねの多い順に並び替えたver






