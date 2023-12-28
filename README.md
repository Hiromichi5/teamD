# teamD

## 動かし方
- config.pyファイルを「teamD / config.py」のように配置する。<br>
- app.pyを実行しブラウザで表示させるとindex.htmlが表示される。<br>
※Dockerの設定はまだなのでflask,requestsなどのインストールが必要

## フロント
- tmplates / index.html<br>
データベースからID,Name,imageを表示させる<br>

### データベースから情報を取得する方法
以下の7つのデータベースの情報を持った変数を用意しました！

- お菓子の虜 APIから取得できる変数(6種類) : snack,chocolate,cookie,candy,rice_cracker,limited_sweets<br>

- Instagram APIから取得できる変数 : instagram


これらの変数はapp.pyからindex.htmlに渡されているので、{{snack.image}}や{{chocolate.name}}のようにアクセスすることで、画像や名前などが取得できます。<br>

### お菓子の虜 API　の変数から取得できる11種類のデータ<br>
|  snack.〇〇  | 意味 |
| ---- | ---- |
|id | ID |
|name | 商品名 |
|kana | ふりがな ※1 |
|maker | メーカー |
|price | 値段 |
|type | 種類 |
|registration_date | 登録日 ※2 |
|url | 商品紹介ページのURL |
|tags | タグ |
|image | 画像のURL |
|comment | 投稿文 |

※1 kanaは結構欠損が多かったので使わない方向で<br>
※2 登録日であって、発売日ではないため不要<br>

'id', 'caption', 'media_url', 'permalink', 'timestamp', 'username', 'followers_count', 'media_count']

### Instagram API　の変数から取得できる8つのデータ<br>
|  instagram.〇〇  | 意味 |
| ---- | ---- |
|id | ID |
|caption | 投稿文 |
|media_url | 画像url |
|permalink| その記事のリンク |
|timestamp | 投稿時間 |
|username | ユーザーの名前 |
|followers_count| フォロワー数 |
|media_count | 投稿数|


## バック
- app.py<br>
データベースに接続し、htmlファイルにデータを渡す<br>
実行すると、URLがターミナルに表示されるのでブラウザで開くと、コンテンツが表示される。

- database.py<br>
データベースの表示や保存など基本操作の関数が入っている。<br>
実行するとsweets.dbが作成される。<br>
※すでに作成されている状態で実行するとうまくいかないため、sweets.dbを消してから実行することを推奨。

-------
ここから下のファイルは実行しない

- sweets.db<br>
 データベース(snack,chocolate,cookie,candy,rice_cracker,limited_sweets,instagramの7つのテーブルがある。)

- sweets_api.py<br>
お菓子の虜APIを動かす。<br>

- instagram_api.py<br>
Instagram APIを動かす。<br>
ひとまず検索するユーザを指定し、最新の10件の投稿をデータベースに登録している。<br>

- config.py<br>
instagram APIを使用するためのビジネスIDとアクセストークンの情報が入っている。<br>
※git hub上に公開することはセキュリティ上の問題があるため各自でteamDディレクトリの配下に置いてください。 

### データベースの構成

| id | name | kana | maker | price | type | registration_date | url | tags | image | comment |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |  ---- | ---- |
| 11291 |  |  |  |  |  |  |  |  |  |  |
| 11277 |  |  |  |  |  |  |  |  |  |  |
| 11262 |  |  |  |  |  |  |  |  |  |  |

sweets.dbには以下の7つのテーブルがある。<br>
Snack : スナック<br>
Chocolate : チョコレート<br>
Cookie : クッキー<br>
Candy : 飴・ガム<br>
Rice_cracker : せんべい・和風<br>
Limited_sweets : 限定品<br>
Instagram : インスタの投稿<br>






