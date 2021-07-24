import requests
import json

def get_current_weather(input):
    API_KEY = "xxxxxxxxxxxxxx"  # xxxに自分のAPI Keyを入力。
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
        api='http://api.openweathermap.org/data/2.5/forecast?lon={lon}&lat={lat}&APPID={key}'
        url = api.format(lon=longitude, lat=latitude, key=API_KEY)
        res = requests.get(url).json()
        return res

if __name__ == "__main__":
    #郵便番号
    postal_code = '466-0827'
    dict = get_current_weather(postal_code)
    print("場所:" + str(dict["city"]['name']))
    for d in dict['list']:
        #時間
        print("時刻: " + str(d['dt_txt']))
        #天気
        print("天気: " + str(d['weather'][0]['description']))
        #湿度
        print("湿度: " + str(d['main']['humidity']) + "[%]")
        #気温
        print("気温: " + str(d['main']['temp']) + "[℃]")
        #曇の割合
        print("雲の割合: " + str(d['clouds']['all']) + "[%]")
        #降水確率
        print("降水確率: " + str(d['pop']) + "[%]")

