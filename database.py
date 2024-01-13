# database.py
# データの登録,削除など
import sqlite3
from datetime import datetime
import instagram_api
import sweets_api
import json
import sys
import tqdm


def create_database():
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
            price INTEGER,
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
            price INTEGER,
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
            price INTEGER,
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
            price INTEGER,
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
            price INTEGER,
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
            price INTEGER,
            type TEXT,
            registration_date DATE,
            url TEXT,
            tags TEXT,
            image TEXT,
            comment TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Instagram (
            id TEXT PRIMARY KEY,
            like_count INTEGER,
            comments_count INTEGER,
            followers_count INTEGER,
            media_count INTEGER,
            caption TEXT,
            media_url TEXT,
            permalink TEXT,
            timestamp TEXT,
            username TEXT
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
    if table_name != "Instagram":
        try:
            # SQLiteデータベースに接続
            conn = sqlite3.connect(database_file)
            cursor = conn.cursor()

            #print("テーブル：",table_name)
            for item in data['item']:
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
                    type_json,
                    datetime.strptime(item['regist'], "%Y年%m月%d日").date(),
                    item['url'],
                    tags_json,
                    item['image'],
                    item.get('comment', '')

                ))
                #print(f'お菓子 {item["id"]} をデータベースに保存しました.')

            conn.commit()
        except Exception as e:
            print(f'データベースへの保存中にエラーが発生しました: {e}')
        finally:
            # データベース接続をクローズ
            if conn:
                conn.close()
    else:
        try:
            #print("テーブル：",table_name)
            # SQLiteデータベースに接続
            conn = sqlite3.connect(database_file)
            cursor = conn.cursor()
            limit = 5# 先頭の10件だけを処理
            for item in data['business_discovery']['media']['data'][:limit]:
                try:
                    media_url_json = None if 'media_url' not in item else str(item['media_url'])
                    # データベースに挿入
                    cursor.execute(f'''
                        INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        item['id'],
                        item['like_count'],
                        item['comments_count'],
                        data['business_discovery']['followers_count'],
                        data['business_discovery']['media_count'],
                        item['caption'],
                        media_url_json,
                        item['permalink'],
                        item['timestamp'],
                        item['username']
                    ))
                    conn.commit()
                    print(f'Instagramデータ {item["id"]} をデータベースに保存しました。')
                except Exception as e:
                    print(f'データベースへの保存中にエラーが発生しました: {e}')
                    print(f'エラーが発生したデータ: {item}')
        except Exception as e:
            print(f'データベースへの接続中にエラーが発生しました: {e}')
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

# instagramテーブルをいいね順に並び替えて新しいテーブルを作成する関数
def create_ordered_table(database_file, source_table, destination_table, order_by_column):
    try:
        # SQLiteデータベースに接続
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # 新しいテーブルを作成
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {destination_table} AS
            SELECT * FROM {source_table}
            ORDER BY {order_by_column} DESC;
        ''')

        # 変更をコミット
        conn.commit()
        print(f'{destination_table} テーブルを作成しました。')

    except Exception as e:
        print(f'テーブルの作成中にエラーが発生しました: {e}')

    finally:
        # データベース接続をクローズ
        if conn:
            conn.close()

#関係のない投稿を削除する関数
def delete_instagram_data_without_any_keyword(database_file):
    try:
        # SQLiteデータベースに接続
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        #チョコ、アイス、和菓子、グミ、
        # 指定された条件に基づいてデータを削除
        cursor.execute('''
            DELETE FROM Instagram
            WHERE NOT (
                (caption LIKE '%発売%'
                OR caption LIKE '%新作%')
                AND NOT (caption LIKE '%スターバックス%' 
                       OR caption LIKE '%マクドナルド%' 
                       OR caption LIKE '%ミスタードーナツ%'
                       OR caption LIKE '%3選%'
                       OR caption LIKE '%レシピ'
                       OR media_url LIKE '%.mp4%')
            );
        ''')

        # 変更をコミット
        conn.commit()
        print('指定されたいずれかのキーワードを含まないInstagramデータを削除しました。')

    except Exception as e:
        print(f'データの削除中にエラーが発生しました: {e}')

    finally:
        # データベース接続をクローズ
        if conn:
            conn.close()

if __name__ == "__main__":
    #create_database()
    # データベースに保存
    #save_data(data, 'Instagram', 'sweets.db')
    #account_list = ['sweetroad7','matchannel_official','seven_eleven_japan','familymart.japan','akiko_lawson','meiji_essel_supercup','calbee_jp','ghana_recipe']
    #account_list = ['yorushika_official_']
    #instagram_api.instagram_to_database(account_list)
    #sweets_api.sweet_to_database()
    #delete_instagram_data_without_any_keyword('sweets.db')
    #create_ordered_table('sweets.db', 'Instagram', 'OrderedInstagram', 'like_count')
    # データベースの内容を表示
    display_database_contents('sweets.db')
