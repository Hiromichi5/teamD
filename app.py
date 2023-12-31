
# app.py

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
        self.link = url
        self.tag = tags
        self.image = image
        self.text = comment

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
        #self.impressions = impressions

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

app = Flask(__name__)

# データベースからデータを取得（例として各テーブルを取得）
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
    return render_template('index.html', snack=snack, chocolate=chocolate, cookie=cookie, candy=candy, japanese=japanese, limited=limited, instagram=instagram)

#@app.route('/chocolate')
#def chocolate():
    # chocolate.htmlにデータを渡して表示
    #return render_template('chocolate.html', chocolate=chocolate_data)

if __name__ == '__main__':
    app.run(debug=True)