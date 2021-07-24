import requests
import json

def get_current_weather(input):
    API_KEY = "0fedfd4841eac192a6d3f3819f1bd491"  # xxxに自分のAPI Keyを入力。
    api = "http://api.openweathermap.org/data/2.5/forecast?zip={code},jp&units=metric&lang=ja&APPID={key}"
    url = api.format(code=input, key=API_KEY)

    # 気象情報を取得
    res = requests.get(url).json()

    if res['message'] != 'city not found':
        return res
    else:
        #郵便番号検索で見つからない場合 => 緯度、経度で検索する
        url = "http://geoapi.heartrails.com/api/json"
        params = {
            "method" : "searchByPostal",
            "postal" : input
        }
        res = requests.get(url,params=params)
        dict = json.loads(res.text)
        longitude = dict["response"]["location"][0]["x"]
        latitude = dict["response"]["location"][0]["y"]
        url='http://api.openweathermap.org/data/2.5/forecast'
        params={
            "lon":longitude,
            "lat":latitude,
            "units":"metric",
            "APPID":"0fedfd4841eac192a6d3f3819f1bd491"
        }
        res = requests.get(url,params=params)
        return res

if __name__ == "__main__":
    #郵便番号
    postal_code = '771-1623'
    dict = json.loads(get_current_weather(postal_code).text)
    print(dict)


