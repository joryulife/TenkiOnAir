import requests
import json
import pykakasi

def GetStreetAdress(postal_code):

    #APIのURL設定
    API = "https://zipcloud.ibsnet.co.jp/api/search?zipcode={code}"
    RECEST_URL = API.format(code=postal_code)

    # 住所情報を取得
    response = requests.get(RECEST_URL)
    jsonText = response.text

    #辞書型に変換
    json_to_dic_result = json.loads(response.text)
    adress_data = json_to_dic_result['results']

    #市区町村名カナをローマ字変換
    kks = pykakasi.kakasi()
    result = kks.convert(adress_data[0]['kana2'])
    return result[0]['passport'].capitalize()

if __name__ == "__main__":
    #郵便番号
    postal_code = '100-0005'
    response = GetStreetAdress(postal_code)
    print(response)