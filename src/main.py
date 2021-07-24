from io import DEFAULT_BUFFER_SIZE
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot.models.events import FollowEvent
from linebot.models.send_messages import ImageSendMessage
import json
import datetime, pytz, random, re

from ..lib import token
from MysqlManager import MysqlConnectorManager
sqladdmin = open('../lib/sqladdmin.json','r')
sqladdmin = json.load(sqladdmin)

app = Flask(__name__)

line_bot_api = LineBotApi(token["CAT"])
handler = WebhookHandler(token["CH"])

# 洗濯物を取り込む予定時刻(乾く時間の計算結果がここに入る)
estimated_time = 16 # <= 仮の値

# jsonファイルから画像のダイレクトアクセスURLを取得
img = open('..\\lib\\images.json')
image_url = json.load(img)
print(image_url)

# 現在日時から季節を算出
dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
dt_h = dt_now.hour
month = dt_now.month
season = (month%12 + 3)//3

def gen_random(min, max):
    if random.random() >= 0.2:
        return min
    else:
        return max

# 友達登録時に送信するメッセージ(随時追加OK)
@handler.add(FollowEvent)
def handle_follow(event):
    send_text = '洗濯物を干す時間を通知します。\n'\
                '何時に通知するか入力してください。\n'\
                'これは時間を送信していただければいつでも変更可能です。\n'\
                '例:AM5:00 -> 5, PM13:00 -> 13\n\n'\
                'また、洗濯物を干したら「干した」\n'\
                '取り込んだら「取り込んだ」と送信してください。'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = send_text)
    )


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    CM = MysqlConnectorManager(user=sqladdmin['user'],
        password=sqladdmin['password'],
        host=sqladdmin['host'],
        database_name=sqladdmin['database'])
    CM.start_connection()

    result = CM.fetch_contents(("select * from USER WHERE UserId=%s"),(event.userId))
    if len(result)==0:
        CM.insert_contents(("insert into USER(UserId,UserName,flag) value(%s,%s,%s)"),(event.userId,event.userName,ASKADDRESS))

def flagroute(event,result,CM):
    if result.flag == "ASKADDRESS":
        #messageがddd-ddd形式かチェックしてADDRESSに格納
        if re.match(r"[0-9]{3}-[0-9]{4}",event.message):
            CM.update_delete_contents(("UPDATE USER SET flag=%s where UserId = %s"),("FLAT",result.UserId))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='郵便番号は ddd-dddd の形で送信してください！'))
        #USAGEMessageを送る
        Message = ''
    elif result.flag == "FLAT":
        if event.message == "干した":
            ScheduledTime = "00:00"
            #取込み予想の計算、メッセージへ　ScheduledTimeに
            CM.update_delete_contents(("UPDATE USER SET flag=%s　ScheduledTime=%s where UserId = %s"),("WaitTakeIn",ScheduledTime,result.UserId))
        elif event.message == "コレクション":
            #DBからコレクションを取得しメッセージへ
            collection_items = CM.fetch_contents(("SELECT CollectionSum FROM USER ORDER BY %s")('ASC'))

            CM.update_delete_contents(("UPDATE USER SET flag=%s where UserId = %s"),("FLAT",result.UserId))
        elif event.message == "リマインド":
            #何時にする？とmessage
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='何時にする？'))
            CM.update_delete_contents(("UPDATE USER SET flag=%s where UserId = %s"),("WaitRemindTime",result.UserId))
        else:
            #USAGEメッセージを送信
            CM.update_delete_contents(("UPDATE USER SET flag=%s where UserId = %s"),("FLAT",result.UserId))
    elif result.flag == "WaitTakeIn":
        if event.message == "取り込んだ":
            #コレクションをランダムで選び、何が貰えたか教える
            if season == 1: # 冬の時
                random_num = gen_random(128, 256)
            elif season == 2: # 春の時
                random_num = gen_random(2, 4)
            elif season == 3: # 夏の時
                random_num = gen_random(8, 16)
            else: # 秋の時
                random_num = gen_random(32, 64)

            fetch_result = CM.fetch_contents(("SELECT * FROM Items WHERE ItemId=%s"),(random_num))
            fetch_url = fetch_result['ImageUrl']
            # コレクションに追加
            newCollectionSum = fetch_result['ImageId']
            # 画像送信
            line_bot_api.broadcast(ImageSendMessage(original_content_url=fetch_url,preview_image_url=fetch_url))
            # newCollectionSum = 0
            #コレクションidを加算して更新　newCollectionSum
            CM.update_delete_contents(("UPDATE USER SET flag=%s CollectionSum=%s where UserId = %s"),("FLAT",newCollectionSum,result.UserId))
        else :
            #USAGEを送る
            Message = ""
    elif result.flag == "WaitRemindTime":
        if re.match(r'([01][0-9]|2[0-1]):[0-5][0-9]',event.message): #だれか正規表現で時刻かどうかみて
            remindTime = event.message
            CM.update_delete_contents(("UPDATE USER SET flag=%s remindTime=%s where UserId = %s"),("FLAT",remindTime,result.UserId))
        else:
            #USAGEを送る
            Message = "USAGE"
    else:
        #USAGEを送る
        Message = "USAGE"

if __name__ == "__main__":
    app.run()
