# database.py
# データの登録,削除など
import sqlite3
from datetime import datetime
import json
import sys

# SQLiteデータベースに接続
conn = sqlite3.connect('sweets.db')
cursor = conn.cursor()

# テーブルの作成（初回のみ実行）
#1:スナック, 2:チョコ, 3:クッキー・洋菓子, 4:飴・ガム, 5:せんべい・和風, 99:限定お菓子
#属性['id', 'name', 'kana', 'maker', 'price', 'type', 'registration_date', 'url', 'tags', 'image', 'comment']
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Snack (
        id TEXT PRIMARY KEY,
        name TEXT,
        kana TEXT,
        maker TEXT,
        price REAL,
        type TEXT,
        registration_date DATE,
        url TEXT,
        tags TEXT,
        image TEXT,
        comment TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Chocolate (
        id TEXT PRIMARY KEY,
        name TEXT,
        kana TEXT,
        maker TEXT,
        price REAL,
        type TEXT,
        registration_date DATE,
        url TEXT,
        tags TEXT,
        image TEXT,
        comment TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cookie (
        id TEXT PRIMARY KEY,
        name TEXT,
        kana TEXT,
        maker TEXT,
        price REAL,
        type TEXT,
        registration_date DATE,
        url TEXT,
        tags TEXT,
        image TEXT,
        comment TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Candy (
        id TEXT PRIMARY KEY,
        name TEXT,
        kana TEXT,
        maker TEXT,
        price REAL,
        type TEXT,
        registration_date DATE,
        url TEXT,
        tags TEXT,
        image TEXT,
        comment TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Rice_cracker (
        id TEXT PRIMARY KEY,
        name TEXT,
        kana TEXT,
        maker TEXT,
        price REAL,
        type TEXT,
        registration_date DATE,
        url TEXT,
        tags TEXT,
        image TEXT,
        comment TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Limited_sweets (
        id TEXT PRIMARY KEY,
        name TEXT,
        kana TEXT,
        maker TEXT,
        price REAL,
        type TEXT,
        registration_date DATE,
        url TEXT,
        tags TEXT,
        image TEXT,
        comment TEXT
    )
''')

conn.commit()
conn.close()

# データベースを全表示する関数
def display_database_contents(database_file):
    try:
        # SQLiteデータベースに接続
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # テーブル一覧を取得
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            print('データベースにテーブルが存在しません。')
            return

        # 各テーブルの内容を出力
        for table in tables:
            table_name = table[0]
            print(f'\nテーブル: {table_name}')
            
            # テーブルの列名を取得
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]
            print(f'列名: {column_names}')

            # テーブルの内容を取得
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()

            if not rows:
                print(f'{table_name} テーブルにデータがありません。')
            else:
                print('データ:')
                for row in rows:
                    print(row)

    except Exception as e:
        print(f'データベースの内容表示中にエラーが発生しました: {e}')
    finally:
        # データベース接続をクローズ
        if conn:
            conn.close()

#テーブルを表示する関数
def display_table_contents(database_file, table_name):
    try:
        # SQLiteデータベースに接続
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # テーブルの内容を取得
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()

        if not rows:
            print(f'{table_name} テーブルにデータがありません。')
        else:
            # テーブルの内容を表示
            print(f'\nテーブル: {table_name}')
            for row in rows:
                print(row)

    except Exception as e:
        print(f'データベースの内容表示中にエラーが発生しました: {e}')
    finally:
        # データベース接続をクローズ
        if conn:
            conn.close()

# データを保存する関数
def save_data(data, table_name, database_file):
    for item in data['item']:
        try:
            # SQLiteデータベースに接続
            conn = sqlite3.connect(database_file)
            cursor = conn.cursor()

            # 空の辞書が返される時はNoneにする
            kana_json = None if isinstance(item['kana'], dict) else item['kana']
            maker_json = None if isinstance(item['maker'], dict) else item['maker']
            price_json = None if isinstance(item['price'], dict) else item['price']
            type_json = None if isinstance(item['type'], dict) else item['type']
            
            # 'tags'が存在しない場合はNoneを登録
            tags_json = None if 'tags' not in item else str(item['tags'])

            # データベースに挿入
            cursor.execute(f'''
                INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item['id'],
                item['name'],
                kana_json,
                maker_json,
                price_json,
                item['type'],
                datetime.strptime(item['regist'], "%Y年%m月%d日").date(),
                item['url'],
                tags_json,
                item['image'],
                item.get('comment', '')
            ))
            conn.commit()
            print(f'お菓子 {item["id"]} をデータベースに保存しました。')
        except Exception as e:
            print(f'データベースへの保存中にエラーが発生しました: {e}')
            print(item)
        finally:
            # データベース接続をクローズ
            if conn:
                conn.close()

# データベースの全ての内容を削除する関数
def clear_database(database_file):
    try:
        # SQLiteデータベースに接続
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # テーブル一覧を取得
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            print(f'データベース {database_file} にテーブルが存在しません。')
            return

        # 各テーブルの内容を削除
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DELETE FROM {table_name};")
            print(f'{table_name} テーブルの内容を削除しました。')

        # 変更をコミット
        conn.commit()

    except Exception as e:
        print(f'データベース {database_file} の内容削除中にエラーが発生しました: {e}')

    finally:
        # データベース接続をクローズ
        if conn:
            conn.close()

#
if __name__ == "__main__":
    #display_database_contents('sweets.db')
    #clear_database('sweets.db')
    #display_database_contents('sweets.db')
    #sys.exit()
    # テストデータ（修正後のお菓子データ）
    #sample = {'id': '11188', 'name': 'チロルすっきりコーヒー', 'kana': {}, 'maker': 'チロルチョコ', 'price': '140', 'type': 'chocolate', 'regist': '2023年7月18日', 'url': 'https://sysbird.jp/toriko/2023/07/18/%e3%83%81%e3%83%ad%e3%83%ab%e3%81%99%e3%81%a3%e3%81%8d%e3%82%8a%e3%82%b3%e3%83%bc%e3%83%92%e3%83%bc/', 'tags': {'tag': ['コーヒー', 'チロル']}, 'image': 'https://sysbird.jp/toriko/wp-content/blogs.dir/2/files/2023/07/11188.jpg', 'comment': '\n<p>新シリーズだろうか？4種ほどぶら下がってたなかから、まずコーヒー味を買ってみた。<br>中にはなにも入ってないタイプのストレートなチロルだ。甘さ控えめで、コーヒーの苦味が感じられるのがいい。食べたあともしばらく口の中がすっきりと、ほろ苦さが持続する。仕事中のリフレッシュに効果ありそうだ。この、効果が「ありそう」という雰囲気はけっこう大事。<br>海のような青に泡のようなデザインもすてき。ほら、コーヒーカップがチロルみたいに四角いの。</p>\n'}
    #sample = {
    #'item': [
    #    {'id': '11291', 'name': 'チロルクリームチーズチョコ', 'kana': {}, 'maker': {}, 'price': '42', 'type': 'chocolate', 'regist': '2023年12月11日', 'url': 'https://sysbird.jp/toriko/2023/12/11/%e3%83%81%e3%83%ad%e3%83%ab%e3%82%af%e3%83%aa%e3%83%bc%e3%83%a0%e3%83%81%e3%83%bc%e3%82%ba%e3%83%81%e3%83%a7%e3%82%b3/', 'tags': {'tag': ['コラボ', 'チロル']}, 'image': 'https://sysbird.jp/toriko/wp-content/blogs.dir/2/files/2023/12/11291.jpg', 'comment': '\n<p>レジ前に置いてあったからチロルと分かったものの、kiri チーズと見間違えてしまいそうになるキューブのパッケージだ。中身もクリームチーズのように白く、チーズチョコのなかにチーズクリームが入ってる。ブルーとシルバーの包み紙2種類あるのも嬉しい。<br>なんでも フランス発の kiri チーズが日本での発売40周年の記念コラボだとか。形が似てるからチロルが選ばれたのだろうか？</p>\n'}, {'id': '11277', 'name': 'チロル金の生もちきなこ', 'kana': {}, 'maker': 'チロルチョコ', 'price': '45', 'type': 'chocolate', 'regist': '2023年10月20日', 'url': 'https://sysbird.jp/toriko/2023/10/20/%e3%83%81%e3%83%ad%e3%83%ab%e9%87%91%e3%81%ae%e7%94%9f%e3%82%82%e3%81%a1%e3%81%8d%e3%81%aa%e3%81%93/', 'tags': {'tag': ['チロル', '季節限定']}, 'image': 'https://sysbird.jp/toriko/wp-content/blogs.dir/2/files/2023/10/11277.jpg', 'comment': '\n<p>きなこ苦手なくせに、レジで見かけつい買ってしまった。北海道産大豆100％「金のきなこ」を使ったチロルである。おなじみのきなこもちとは関係ないのだろうか？もちくんの顔もないし、もちはグミではなく生もちというから、値段からして別格なんだろうな。<br>なぜか匂いも味もキャラメルっぽい、香ばしさがそう思わせるのか？「金のきなこ」の特徴は細かい粒子というものの、チョコになってるからわからないではないか。きっと、きなこ好きが食べたら違いに気づくんでは。</p>\n'}, {'id': '11262', 'name': 'ZEROカカオ70%', 'kana': {}, 'maker': 'ロッテ', 'price': '238', 'type': 'chocolate', 'regist': '2023年10月18日', 'url': 'https://sysbird.jp/toriko/2023/10/18/zero%e3%82%ab%e3%82%ab%e3%82%aa70/', 'image': 'https://sysbird.jp/toriko/wp-content/blogs.dir/2/files/2023/10/11262.jpg', 'comment': '\n<p>会社に出勤してたころは、午前中にチョコ1箱を食べていた。朝は元気が出ない理由をつけて、ボリボリ食べていた。おそらくは通勤でカロリーを消費してたからだろうか、そのせいで太ることもなかった。<br>在宅ワークになったいま、チョコを買うこと自体が珍しくなった。チロルの新製品を見かけると買うぐらいは、以前に比べるとかわいい行いだ。そんな折、急にチョコを食べたくなった。ZERO というのと、カカオ70%で罪悪感が薄れるのでこれにした。疲れているのだろうか？カカオ率が高いほうがカロリーは多いのだけど、実質0でしょう。<br>長細い5本入り。</p>\n'}, {'id': '11241', 'name': 'チロルねないこだれだまっくろソフトクリームチロル', 'kana': {}, 'maker': 'チロルチョコ', 'price': '38', 'type': 'chocolate', 'regist': '2023年9月19日', 'url': 'https://sysbird.jp/toriko/2023/09/19/%e3%83%81%e3%83%ad%e3%83%ab%e3%81%ad%e3%81%aa%e3%81%84%e3%81%93%e3%81%a0%e3%82%8c%e3%81%a0%e3%81%be%e3%81%a3%e3%81%8f%e3%82%8d%e3%82%bd%e3%83%95%e3%83%88%e3%82%af%e3%83%aa%e3%83%bc%e3%83%a0%e3%83%81/', 'tags': {'tag': ['コラボ', 'チロル']}, 'image': 'https://sysbird.jp/toriko/wp-content/blogs.dir/2/files/2023/09/11241.jpg', 'comment': '\n<p>絵本「ねないこだれだ」のイラストがついたチロル。10種類あるという図柄から、印象に残ってる3粒を選んだ。表紙だったと覚えてる、白いおばけのポーズが少し違うような？<br>味はまっくろソフトクリーム、チョコも真っ黒で、もしかしたらもうハロウィーン向けかしら。真っ黒なチョコの中にはマシュマロと甘いベリーのソースが入ってる。このマシュマロは、たぶんおばけなのよ(適当〜)<br>裏を見ると、絵本の文章が少しずる書いてある。<br>たぶんファミマ限定</p>\n'}, {'id': '11193', 'name': 'チョコぬいじゃった！きのこの山', 'kana': {}, 'maker': '明治製菓', 'price': '216', 'type': 'chocolate', 'regist': '2023年8月3日', 'url': 'https://sysbird.jp/toriko/2023/08/03/%e3%83%81%e3%83%a7%e3%82%b3%e3%81%ac%e3%81%84%e3%81%98%e3%82%83%e3%81%a3%e3%81%9f%ef%bc%81%e3%81%8d%e3%81%ae%e3%81%93%e3%81%ae%e5%b1%b1/', 'tags': {'tag': ['きのこの山', '夏', '季節限定']}, 'image': 'https://sysbird.jp/toriko/wp-content/blogs.dir/2/files/2023/07/11193.jpg', 'comment': '\n<p>誰もが目を疑ったろう。きのこの主たる食用はカサにありながら、チョコぬいだらただの軸ではないか。スーパーで軸だけ売ってるきのこなんて皆無だ。<br>きのこの山の軸、つまりクッキー部分だけが60本ほどはいってるという。当本舗がきのこ派たるゆえんは、このカリッとした軸にある。チョコがあろうがなかろうが、きのこ派としてついて行かねばなるまい。だが、60本も食べられるのか？心配しつつ、ポリポリと意外に行ける。あっというまに食べ尽くしてしまった。やはりこの軸が好きなのだ。この季節にさっぱりしてるのがいい。<br>夏限定だろうか？もっと食べたい！<br></p>\n'}, {'id': '11188', 'name': 'チロルすっきりコーヒー', 'kana': {}, 'maker': 'チロルチョコ', 'price': '140', 'type': 'chocolate', 'regist': '2023年7月18日', 'url': 'https://sysbird.jp/toriko/2023/07/18/%e3%83%81%e3%83%ad%e3%83%ab%e3%81%99%e3%81%a3%e3%81%8d%e3%82%8a%e3%82%b3%e3%83%bc%e3%83%92%e3%83%bc/', 'tags': {'tag': ['コーヒー', 'チロル']}, 'image': 'https://sysbird.jp/toriko/wp-content/blogs.dir/2/files/2023/07/11188.jpg', 'comment': '\n<p>新シリーズだろうか？4種ほどぶら下がってたなかから、まずコーヒー味を買ってみた。<br>中にはなにも入ってないタイプのストレートなチロルだ。甘さ控えめで、コーヒーの苦味が感じられるのがいい。食べたあともしばらく口の中がすっきりと、ほろ苦さが持続する。仕事中のリフレッシュに効果ありそうだ。この、効果が「ありそう」という雰囲気はけっこう大事。<br>海のような青に泡のようなデザインもすてき。ほら、コーヒーカップがチロルみたいに四角いの。</p>\n'}, {'id': '11175', 'name': 'チロルカヌレ', 'kana': {}, 'maker': 'チロルチョコ', 'price': '31', 'type': 'chocolate', 'regist': '2023年6月23日', 'url': 'https://sysbird.jp/toriko/2023/06/23/%e3%83%81%e3%83%ad%e3%83%ab%e3%82%ab%e3%83%8c%e3%83%ac/', 'tags': {'tag': 'チロル'}, 'image': 'https://sysbird.jp/toriko/wp-content/blogs.dir/2/files/2023/06/11175.jpg', 'comment': '\n<p>やだ、おいしい！このカヌレ感はどこからきてるんだろう？<br>まずラム酒 (アルコール分0.03%) の風味、次にキャラメルっぽいコク。極めつけは、カヌレ最大の特徴であるモチモチ感をあらわしたグミだろう。<br>カヌレはフランス生まれの焼き菓子で、デパ地下やコンビニスイーツとしても人気だ。チロルのパッケージは赤と青の他に白もあった。フランスのトリコロールをイメージしているのか。レジに置いてあるのを会計時に慌てて2粒だけ手に取ったのだ。3色買うべきだった。</p>\n'}, {'id': '11165', 'name': 'チロルベトナムコーヒー', 'kana': {}, 'maker': 'チロルチョコ', 'price': '32', 'type': 'chocolate', 'regist': '2023年6月8日', 'url': 'https://sysbird.jp/toriko/2023/06/08/%e3%83%81%e3%83%ad%e3%83%ab%e3%83%99%e3%83%88%e3%83%8a%e3%83%a0%e3%82%b3%e3%83%bc%e3%83%92%e3%83%bc/', 'tags': {'tag': ['コーヒー', 'チロル']}, 'image': 'https://sysbird.jp/toriko/wp-content/blogs.dir/2/files/2023/06/11165.jpg', 'comment': '\n<p>少し苦めで濃いコーヒー味がクリーム味を包んでいる。鮮やかな花柄や、ランタンのモチーフにキュッと心つかまれるパッケージだ。このたびチロルチョコの工場がベトナムにできたことを記念しているとのこと。<br>ベトナム料理店で飲んだことのあるコーヒーも、濃いめのコーヒーに甘すぎるほどの練乳を注いで飲む形式で、苦さと甘さを楽むものだった。そのコントラストがうまくでているチロルだ。コーヒー味というのも元祖チロル(コーヒーヌガー)に通ずるものがあり、納得の一粒といえよう。<br>包み紙のバリエーションはもっとあるよう、近所のファミマで見かけたときにはこの2種があった。</p>\n'}, {'id': '11160', 'name': '令和チロル', 'kana': {}, 'maker': 'チロルチョコ', 'price': '130', 'type': 'chocolate', 'regist': '2023年6月6日', 'url': 'https://sysbird.jp/toriko/2023/06/06/%e4%bb%a4%e5%92%8c%e3%83%81%e3%83%ad%e3%83%ab/', 'image': 'https://sysbird.jp/toriko/wp-content/blogs.dir/2/files/2023/06/11160.jpg', 'comment': '\n<p>まだ令和になって5年めでありながら、令和チロルには入ったのはピスタチオとマリトッツォだ。<br>マリトッツォか！パンに生クリームをはさんだけでものすごいブームだった。何度も食べたな。チロルではパンっぽい色のチョコでクリーム味を挟んだ、なぜかキャラメルっぽい味。<br>ピスタチオはブームを通り越して安定の人気がある味といえよう。うす緑色のチロルのなかには、ピスタチオのかけらがたまに入ってる。<br>パッケージに描かれているのは、アマビエ、携帯扇風機、「推ししか勝たん」うちわ。</p>\n'}, {'id': '11148', 'name': '平成チロル', 'kana': {}, 'maker': 'チロルチョコ', 'price': '130', 'type': 'chocolate', 'regist': '2023年6月1日', 'url': 'https://sysbird.jp/toriko/2023/06/01/%e5%b9%b3%e6%88%90%e3%83%81%e3%83%ad%e3%83%ab/', 'tags': {'tag': ['タピオカ', 'チロル', 'ティラミス']}, 'image': 'https://sysbird.jp/toriko/wp-content/blogs.dir/2/files/2023/05/11148.jpg', 'comment': '\n<p><a href="https://sysbird.jp/toriko/?p=11129">昭和チロル</a>に続いて平成チロルは、タピオカミルクティーとティラミスの組み合わせだ。<br>数年前にタピオカミルクティーが大流行して、コロナが落ち着いたいまほとんどのタピオカ屋は消えた。タピオカはそれよりもずっと前に流行ってた気がして、振り返ったところ平成にも大ブームがあった。そうタピオカは平成なのだ。プニプニのもちグミはチロルならでは。<br>そしてティラミス！<br>いまでこそ定番スイーツのティラミスも、90年代のブームからきている。とにかくおいしくて特別だったのだ。このチロルも、上層の濃いココア味に対して下層にクリームチーズ特有の香りがあり、ばつぐんの出来だ。ひとつぶのチョコを口にいれただけで、いろんな出来事が思い起こされる。</p>\n'}
    #],
    #'status': 'OK',
    #'count': '10'
    #}

    # テストデータを保存
    #save_data(sample,'Chocolate','sweets.db')

    # データベースの内容を表示
    display_database_contents('sweets.db')

