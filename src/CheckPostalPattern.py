import re
import requests
import json

def CheckExistence(input):
    url = "http://geoapi.heartrails.com/api/json"
    params = {
        "method" : "searchByPostal",
        "postal" : input
    }
    res = requests.get(url,params=params)
    dict = json.loads(res.text)
    return 'error' in dict['response']

def CheckFormat(input):
    #数字7桁「ddddddd」　or　郵便番号のフォーマット「ddd-dddd」
    if re.fullmatch(r"\d{7}", input) != None:
        input = str(input)[0:3] + '-' + str(input)[3:]
    result = re.search(r"\d{3}[-]\d{4}", input)
    if result != None:
        return CheckExistence(input)
    else:
        return False


if __name__ == "__main__":
    #郵便番号
    input = "466-0827"
    if CheckFormat(input):
        print("入力が不正です")
    else:
        print("登録しました")

