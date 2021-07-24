import requests
import json
import datetime

#OpenWeatherAPIの呼び出し
def GetWeather(input):
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
        api='http://api.openweathermap.org/data/2.5/forecast?lon={lon}&lat={lat}&APPID={key}'
        url = api.format(lon=longitude, lat=latitude, key=API_KEY)
        res = requests.get(url).json()
        return res

#天気のパラメータ
def SetWeatherWeight(dict):
    weather = int(dict['weather'][0]['id'])
    #天気の場合分け
    if 700 > weather:
        add = 2.0
    elif 800 == weather:
        add = 1.0
    elif 801 == weather:
        add = 1.2
    elif 802 == weather:
        add = 1.5
    elif 803 == weather:
        add = 1.7
    elif 804 == weather:
        add = 1.8
    return add

#気温のパラメータ
def SetTemperatureWeight(dict):
    temperature = int(d['main']['temp'])
    if 8 > temperature:
        add = 2.0
    elif 12 > temperature:
        add = 1.9
    elif 17 > temperature:
        add = 1.8
    elif 22 > temperature:
        add = 1.7
    elif 25 > temperature:
        add = 1.6
    elif 27 > temperature:
        add = 1.4
    elif 30 > temperature:
        add = 1.2
    else:
        add = 1.0
    return add

"""メイン関数 : 開始時間[datetime]と郵便番号[str]を引数 ==> return 予定時刻[datetime]"""
def GetScheduledTime(start_time,postal_code):
    #jsonデータを取得
    dict = GetWeather(postal_code)
    #weightを計算
    weather_sum = 0
    temperature_sum = 0
    #現在時刻より未来のデータ4つ分(12時間)を使う
    i = 0
    for d in dict['list']:
        dict_time = datetime.datetime.strptime(d['dt_txt'], '%Y-%m-%d %H:%M:%S')
        if dict_time > dt_now:
            print(dict_time)
            i += 1
        if i > 3:
            break
        weather_sum += SetWeatherWeight(d)
        temperature_sum += SetTemperatureWeight(d)
    #計算式
    add_hours = round(3.0*(weather_sum/6.0)*(temperature_sum/6.0),1)
    #datetime型で予定時刻を返す
    return dt_now + datetime.timedelta(hours=add_hours)