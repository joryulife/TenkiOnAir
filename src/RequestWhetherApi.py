import requests
import json

def get_current_weather(postal_code):
    API_KEY = "xxxxxxxxxxxxxxxxxxx"  # xxxに自分のAPI Keyを入力。
    api = "http://api.openweathermap.org/data/2.5/forecast?zip={code},jp&units=metric&lang=ja&APPID={key}"

    url = api.format(code=postal_code, key=API_KEY)

    # 気象情報を取得
    response = requests.get(url).json()
    # APIレスポンスの表示
    jsonText = json.dumps(response, indent=2)
    print(jsonText)

    return response


if __name__ == "__main__":
    # 住所を指定する。
    postal_code = '100-0005'  #東京都千代田区(すべての住所に対応していないため一部地域ではレスポンスがnot foundになる)
    response = get_current_weather(postal_code)
