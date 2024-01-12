import requests
import database

url = "https://sysbird.jp/toriko/api/"
api_key = "guest"  # ここに実際のAPIキーを追加してください
sweets_type = [1, 2, 3, 4, 5, 99]
table_names = ['Snack', 'Chocolate', 'Cookie', 'Candy', 'Rice_cracker', 'Limited_sweets']
def sweet_to_database():
    for i, table_name in zip(sweets_type, table_names):
        params = {"apikey": api_key, "format": "json", "type": i, "max":30}
        #type
        #1:スナック, 2:チョコ, 3:クッキー・洋菓子, 4:飴・ガム, 5:せんべい・和風, 99:限定お菓子
        try:
            # お菓子の虜 APIにリクエストを送信
            print("お菓子の虜 APIにリクエストを送信中("+str(table_name)+")")
            response = requests.get(url, params=params)

            # レスポンスが成功 (HTTP ステータスコード 200) の場合
            if response.status_code == 200:
                try:
                    # レスポンスからお菓子情報を取得
                    data = response.json()
                    # テストデータを保存
                    database.save_data(data,table_name,'sweets.db')
                    # 菓子名・メーカーの表示
                    #print("菓子名・メーカー:")
                    #for item in data.get("item", []):
                    #    print(item.get("name", "None"), item.get("maker", "None"))

                except ValueError as json_error:
                    # JSON データが正しくない場合
                    print(f"Web API からのレスポンスが正しい JSON フォーマットではありません。エラー: {json_error}")

            else:
                # レスポンスが失敗の場合
                print(f"Web API リクエストが失敗しました。ステータスコード: {response.status_code}")

        except Exception as e:
            print(f"エラーが発生しました: {e}")
if __name__ == "__main__":
    # データベースの内容を表示
    database.display_database_contents('sweets.db')

#レスポンスの例
#{ 'id': '11241',
#  'name': 'チロルねないこだれだまっくろソフトクリームチロル', 
#  'kana': {}, 
#  'maker': 'チロルチョコ', 
#  'price': '38', 
#  'type': 'chocolate', 
#  'regist': '2023年9月19日', 
#  'url': 'https://sysbird.jp/toriko/2023/09/19/%e3%83%81%e3%83%ad%e3%83%ab%e3%81%ad%e3%81%aa%e3%81%84%e3%81%93%e3%81%a0%e3%82%8c%e3%81%a0%e3%81%be%e3%81%a3%e3%81%8f%e3%82%8d%e3%82%bd%e3%83%95%e3%83%88%e3%82%af%e3%83%aa%e3%83%bc%e3%83%a0%e3%83%81/', 
#  'tags': {'tag': ['コラボ', 'チロル']}, 
#  'image': 'https://sysbird.jp/toriko/wp-content/blogs.dir/2/files/2023/09/11241.jpg', 
#  'comment': '\n<p>絵本「ねないこだれだ」のイラストがついたチロル。10種類あるという図柄から、印象に残ってる3粒を選んだ。表紙だったと覚えてる、白いおばけのポーズが少し違うような？<br>味はまっくろソフトクリーム、チョコも真っ黒で、もしかしたらもうハロウィーン向けかしら。真っ黒なチョコの中にはマシュマロと甘いベリーのソースが入ってる。このマシュマロは、たぶんおばけなのよ(適当〜)<br>裏を見ると、絵本の文章が少しずる書いてある。<br>たぶんファミマ限定</p>\n'}
