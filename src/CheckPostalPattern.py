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
    if 'error' in dict['response']:
        #存在しない場合
        return 1
    else:
        #エラーがない場合
        return 0
    
def CheckFormat(input):
    #数字7桁「ddddddd」　or　郵便番号のフォーマット「ddd-dddd」
    if re.fullmatch(r"\d{7}", input) != None:
        input = str(input)[0:3] + '-' + str(input)[3:]
    result = re.search(r"\d{3}[-]\d{4}", input)
    if result != None:
        return CheckExistence(input)
    else:
        #formatが不正
        return 2

def CheckPostalCode(postal_code):
    #0:問題なし, 1:住所が存在しない, 2:フォーマットが不正
    return CheckFormat(input)