# app.py
import database
import sqlite3
from flask import Flask, render_template

class Sweets:
    def __init__(self, id, name, kana, maker, price, type, registration_date, url, tags, image, comment):
        self.id = id
        self.name = name
        self.kana = kana
        self.maker = maker
        self.price = price
        self.type = type
        self.date = registration_date
        self.url = url
        self.tags = tags
        self.image = image
        self.comment = comment

class Insta:
    def __init__(self, id, like_count, comments_count,followers_count, media_count,caption, media_url, permalink, timestamp, username):
        self.id = id
        self.text = caption
        self.image = media_url
        self.link = permalink
        self.date = timestamp
        self.username = username
        self.follower = followers_count
        self.post = media_count
        self.like = like_count
        self.comment = comments_count

def get_data_from_database(table_name):
    # SQLiteデータベースに接続
    connection = sqlite3.connect('sweets.db')
    cursor = connection.cursor()

    # データベースから情報を取得（適切なSQLクエリを使用する）
    cursor.execute(f'SELECT * FROM {table_name}')
    data = cursor.fetchall()

    # 接続を閉じる
    connection.close()
    if table_name != 'OrderedInstagram':
        # Sweetsクラスのインスタンスを生成してリストに追加
        sweets_list = [Sweets(*item) for item in data]
    else:
        sweets_list = [Insta(*item) for item in data]

    return sweets_list

if __name__ == '__main__':
    #　データベースを0から作成する
    # database.make_new_database()
    
    #　データベースを更新する
    database.update_database()
    
    print("---------------------")

    app = Flask(__name__, static_folder="./static/")

    # データベースからデータを取得
    snack = get_data_from_database('Snack')
    chocolate = get_data_from_database('Chocolate')
    cookie = get_data_from_database('Cookie')
    candy = get_data_from_database('Candy')
    japanese = get_data_from_database('Rice_cracker')
    limited = get_data_from_database('Limited_sweets')
    instagram = get_data_from_database('OrderedInstagram')

    @app.route('/')
    def index():
        # index.htmlにデータを渡して表示
        return render_template('index.html', instagram=instagram)

    @app.route('/snack')
    def snack_detail():
        # chocolate.htmlにデータを渡して表示
        return render_template('detail.html', items = snack, genre='snack')


    @app.route('/chocolate')
    def choco_detail():
        # chocolate.htmlにデータを渡して表示
        return render_template('detail.html',items = chocolate, genre='choco')


    @app.route('/cookie')
    def cookie_detail():
        # chocolate.htmlにデータを渡して表示
        return render_template('detail.html', items = cookie, genre='cookie')


    @app.route('/candy')
    def candy_detail():
        # chocolate.htmlにデータを渡して表示
        return render_template('detail.html', items = candy, genre='candy')


    @app.route('/japanese')
    def japanese_detail():
        # chocolate.htmlにデータを渡して表示
        return render_template('detail.html', items = japanese, genre='japanese')


    @app.route('/limited')
    def limited_detail():
        # chocolate.htmlにデータを渡して表示
        return render_template('detail.html', items=limited, genre='limited')
    
    app.run(host='0.0.0.0', port=8080)