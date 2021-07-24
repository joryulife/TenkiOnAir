
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

import CheckPostalPattern
import RequestWhetherApi

token = open('../lib/token.json','r')
token = json.load(token)
from linebot.models.events import FollowEvent
from linebot.models.send_messages import ImageSendMessage
import json
import datetime, random, pytz, re
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
# 取り込んだ時に送信する画像選択用の乱数
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
    else:
        flagroute(event,result,CM)

def flagroute(event,result,CM):
    if result.flag == "ASKADDRESS":
        #messageがddd-ddd形式かチェックしてADDRESSに格納
        postal_res = CheckPostalPattern.CheckPostalCode(event.message.text)
        if postal_res == 0:
            CM.update_delete_contents(("UPDATE USER SET flag=%s where UserId = %s"),("FLAT",result.UserId))
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="郵便番号を登録しました。"))
        elif postal_res == 1:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="存在する郵便番号を入力してください。"))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="郵便番号は●●●-●●●●(ハイフンなしも可)で送信してください。"))
        #USAGEMessageを送る
    elif result.flag == "FLAT":
        if event.message.text == "干した":
            dt_now = datetime.datetime.now()
            postal_code = CM.fetch_contents(("SELECT Uaddress　FROM USER WHERE UserId = %s"),(result.UserId))
            ScheduledTime = RequestWhetherApi.GetScheduledTime(dt_now,postal_code)
            #取込み予想の計算、メッセージへ　ScheduledTimeに
            CM.update_delete_contents(("UPDATE USER SET flag=%s　ScheduledTime=%s where UserId = %s"),("WaitTakeIn",ScheduledTime,result.UserId))
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='洗濯物が乾く時間は' + dt_now.strftime('%m月%d日 %H時%M分です。')))
        elif event.message.text == "コレクション":
            collection_items = CM.fetch_contents(("SELECT CollectionSum FROM USER ORDER BY %s")('ASC'))
            for item_url in collection_items:
                line_bot_api.broadcast(ImageSendMessage(original_content_url=item_url, preview_image_url=item_url))
            #DBからコレクションを取得しメッセージへ
            CM.update_delete_contents(("UPDATE USER SET flag=%s where UserId = %s"),("FLAT",result.UserId))
        elif event.message.text == "リマインド":
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='何時にする？'))
            CM.update_delete_contents(("UPDATE USER SET flag=%s where UserId = %s"),("WaitRemindTime",result.UserId))
        else:
            #USAGEメッセージを送信
            usage = '「干した」と送信すると、\n'\
                    '洗濯物を取り込む時間をお知らせします。\n'\
                    '「コレクション」と送信すると\n'\
                    '今までに取得した花の画像が見れます。\n'\
                    '「リマインド」と送信すると\n'\
                    'リマインドの時間を変更できます。\n'\
                    'リマインドは洗濯物を干す時間を促すものです。'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=usage))
            CM.update_delete_contents(("UPDATE USER SET flag=%s where UserId = %s"),("FLAT",result.UserId))
    elif result.flag == "WaitTakeIn":
        if event.message.text == "取り込んだ":
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
            #コレクションidを加算して更新　newCollectionSum
            CM.update_delete_contents(("UPDATE USER SET flag=%s CollectionSum=%s where UserId = %s"),("FLAT",newCollectionSum,result.UserId))
        else :
            #USAGEを送る
            usage = 'もし洗濯物を取り込んだら、「取り込んだ」と送信してください。'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=usage))
    elif result.flag == "WaitRemindTime":
        if re.match(r'([01][0-9]|2[0-1]):[0-5][0-9]',event.message.text):#だれか正規表現で時刻かどうかみて
            remindTime = event.message.text
            CM.update_delete_contents(("UPDATE USER SET flag=%s remindTime=%s where UserId = %s"),("FLAT",remindTime,result.UserId))
        else:
            #USAGEを送る
            usage = "リマインド時刻は、\n「00:00」のように送信してください。"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=usage))
    else:
        #USAGEを送る
        usage = "エラーが起きました！！"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=usage))

if __name__ == "__main__":
    app.run()
