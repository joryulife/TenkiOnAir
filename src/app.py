
import json
from flask import Flask, request, abort
from MysqlManager import MysqlConnectorManager
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

from MysqlManager import MysqlConnectorManager

token = open('../lib/token.json','r')
token = json.load(token)
from linebot.models.events import FollowEvent
from linebot.models.send_messages import ImageSendMessage
import json
import datetime, random,pytz
from MysqlManager import MysqlConnectorManager

sqladdmin = open('../lib/sqladdmin.json','r')
sqladdmin = json.load(sqladdmin)
CM = MysqlConnectorManager(user=sqladdmin['user'],
    password=sqladdmin['password'],
    host=sqladdmin['host'],
    database_name=sqladdmin['database'])
CM.start_connection()

app = Flask(__name__)
token = open('../lib/token.json','r')
token = json.load(token)
line_bot_api = LineBotApi(token["CAT"])
handler = WebhookHandler(token["CH"])

# 現在日時から季節を算出
dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
dt_h = dt_now.hour
month = dt_now.month
season = (month%12 + 3)//3

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
    print("callback in")
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    CM = MysqlConnectorManager(user=sqladdmin['user'],
        password=sqladdmin['password'],
        host=sqladdmin['host'],
        database_name=sqladdmin['database'])
    CM.start_connection()
    print(event.source.user_id)
    #event.source.user_id
    q = "SELECT * FROM USER WHERE UserId=%s"
    ps = (event.source.user_id, )
    result = CM.fetch_contents(q,ps)
    if len(result)==0:
        CM.insert_contents(("insert into USER (UserId,flag) values (%s,%s)"),(event.source.user_id,"ASKADDRESS"))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ddd-dddd 形式で郵便番号を入力してください。"))

def flagroute(event,result,CM):
    if result.flag == "ASKADDRESS":
        #messageがddd-ddd形式かチェックしてADDRESSに格納
        CM.update_delete_contents(("UPDATE USER SET flag=%s where UserId = %s"),("FLAT",result.UserId))
        #USAGEMessageを送る
    elif result.flag == "FLAT":
        if event.message == "干した":
            ScheduledTime = "00:00"
            #取込み予想の計算、メッセージへ　ScheduledTimeに
            CM.update_delete_contents(("UPDATE USER SET flag=%s　ScheduledTime=%s where UserId = %s"),("WaitTakeIn",ScheduledTime,result.UserId))
        elif event.message == "コレクション":
            #DBからコレクションを取得しメッセージへ
            CM.update_delete_contents(("UPDATE USER SET flag=%s where UserId = %s"),("FLAT",result.UserId))
        elif event.message == "リマインド":
            #何時にする？とmessage
            CM.update_delete_contents(("UPDATE USER SET flag=%s where UserId = %s"),("WaitRemindTime",result.UserId))
        else:
            #USAGEメッセージを送信
            CM.update_delete_contents(("UPDATE USER SET flag=%s where UserId = %s"),("FLAT",result.UserId))
    elif result.flag == "WaitTakeIn":
        if event.message == "取り込んだ":
            #コレクションをランダムで選び、何が貰えたか教える
            newCollectionSum = 0
            #コレクションidを加算して更新　newCollectionSum
            CM.update_delete_contents(("UPDATE USER SET flag=%s CollectionSum=%s where UserId = %s"),("FLAT",newCollectionSum,result.UserId))
        else :
            #USAGEを送る
            Message = ""
    elif result.flag == "WaitRemindTime":
        if event.message == "00:00":#だれか正規表現で時刻かどうかみて
            remindTime = ""
            CM.update_delete_contents(("UPDATE USER SET flag=%s remindTime=%s where UserId = %s"),("FLAT",remindTime,result.UserId))
        else:
            #USAGEを送る
            Message = "USAGE"
    else:
        #USAGEを送る
        Message = "USAGE" 

if __name__ == "__main__":
    app.run()
