# teamD

## 動かし方
app.pyを実行しブラウザで表示させるとindex.htmlが表示される。<br>
Dockerの設定はまだなのでflask,requestsなどのインストールが必要

## フロント
- tmplates / index.html<br>
データベースからID,Name,imageを表示させる<br>

### データベースから情報を取得する方法

6種類のお菓子変数 : snack,chocolate,cookie,candy,rice_cracker,limited_sweetsがapp.pyからindex.htmlに渡されているので、{{snack.image}}や{{chocolate.name}}とすることで、それぞれスナック菓子の画像、チョコの名前が取得できます。<br>

#### 取得できる情報<br>
|    | 意味 |
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
※2 登録日であって、発売日ではないため不要



## バック
- app.py<br>
データベースに接続し、htmlファイルにデータを渡す

- sweets.db<br>
 データベース

- database.py<br>データベースの表示や保存など基本操作の関数が入っている

- sweets_api.py<br>
お菓子の虜APIを動かす<br>
このファイルを実行すると、sweets.dbが作成される

### データベースの構成

| id | name | kana | maker | price | type | registration_date | url | tags | image | comment |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |  ---- | ---- |
| 11291 |  |  |  |  |  |  |  |  |  |  |
| 11277 |  |  |  |  |  |  |  |  |  |  |
| 11262 |  |  |  |  |  |  |  |  |  |  |

お菓子の虜APIの都合で、6種類(Snack,Chocolate,Cookie,Candy,Rice_Cracker,Limited_sweets)のテーブルを作成し、1つのデータベースファイルsweets.dbにまとめている。









