# instagram.py
import sys
import requests
import json
import database
from config import INSTA_BUSINESS_ID, ACCESS_TOKEN
insta_business_id = INSTA_BUSINESS_ID
access_token = ACCESS_TOKEN
# Instagram APIでプロファイル情報を取得する関数
def instagram_basic_display_api_profile(insta_business_id, access_token):
    url = f'https://graph.facebook.com/v17.0/{insta_business_id}/?fields=name,media_count,username,id,profile_picture_url&access_token={access_token}'

    try:
        response = instagram_api(url, 'GET', access_token)
        if response:
            data = response.json()
            print(data)
            return data
        else:
            print('Instagram APIのリクエストでエラーが発生しました。')
            return None
    except Exception as error:
        print('Instagram APIのレスポンスの解析中にエラーが発生しました:', error)
        return None

def instagram_to_database(account_list):
    for account in account_list:
        business_discovery_api(account)

# ビジネスディスカバリーAPIを叩く関数
def business_discovery_api(insta_account_name):
    
    url = f'https://graph.facebook.com/v17.0/{insta_business_id}?fields=business_discovery.username({insta_account_name})%7Bfollowers_count,media_count,media.limit(5)%7Bcaption,media_url,permalink,timestamp,username,like_count,comments_count,children%7Bmedia_url%7D%7D%7D&access_token={access_token}'

    try:
        print("Instagram APIにリクエストを送信中("+str(insta_account_name)+")")
        response = instagram_api(url, 'GET', '')
        if response:
            data = response.json()
            #print(data)  # 返り値①
            #print(data['business_discovery']['media']['data'])  # 返り値②
            #print(data)
            #sys.exit()
            database.save_data(data,'Instagram','sweets.db')
            return data
        else:
            print('Instagram APIのリクエストでエラーが発生しました。')
            return None
    except Exception as error:
        print('Instagram APIのレスポンスの解析中にエラーが発生しました:', error)
        return None

# APIを叩く関数
def instagram_api(url, method, access_token):
    try:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        return response
    except Exception as error:
        print('Instagram APIのリクエスト中にエラーが発生しました:', error)
        return None

if __name__ == "__main__":
    # ビジネスアカウントIDとアクセストークンを設定
    #insta_account_name = 'sweetroad7'  # 取得したいアカウントID名
    account_list = ['sweetroad7']
    # Instagram APIでプロファイル情報を取得
    # instagram_basic_display_api_profile(INSTA_BUSINESS_ID, ACCESS_TOKEN)
    #print(business_discovery_api(insta_account_name))
    instagram_to_database(account_list)
