
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
        self.registration_date = registration_date
        self.url = url
        self.tags = tags
        self.image = image
        self.comment = comment

def get_data_from_database(table_name):
    # SQLiteデータベースに接続
    connection = sqlite3.connect('sweets.db')
    cursor = connection.cursor()

    # データベースから情報を取得（適切なSQLクエリを使用する）
    cursor.execute(f'SELECT * FROM {table_name}')
    data = cursor.fetchall()

    # 接続を閉じる
    connection.close()

    # Sweetsクラスのインスタンスを生成してリストに追加
    sweets_list = [Sweets(*item) for item in data]

    return sweets_list

app = Flask(__name__)

@app.route('/')
def index():
    # データベースからデータを取得（例として各テーブルを取得）
    snack = get_data_from_database('Snack')
    chocolate = get_data_from_database('Chocolate')
    cookie = get_data_from_database('Cookie')
    candy = get_data_from_database('Candy')
    rice_cracker = get_data_from_database('Rice_cracker')
    limited_sweets = get_data_from_database('Limited_sweets')

    # index.htmlにデータを渡して表示
    return render_template('index.html', snack=snack, chocolate=chocolate, cookie=cookie, candy=candy, rice_cracker=rice_cracker, limited_sweets=limited_sweets)


if __name__ == '__main__':
    app.run(debug=True)