# app.py

import sqlite3
from flask import Flask, render_template

def get_data_from_database():
    # SQLiteデータベースに接続
    connection = sqlite3.connect('instagram_posts.db')
    cursor = connection.cursor()

    # データベースから情報を取得（適切なSQLクエリを使用する）
    cursor.execute('SELECT * FROM instagram_posts')
    data = cursor.fetchall()

    # 接続を閉じる
    connection.close()

    return data

app = Flask(__name__)

@app.route('/')
def index():
    # データベースからデータを取得
    data = get_data_from_database()

    # index.htmlにデータを渡して表示
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
