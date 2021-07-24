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
import datetime, pytz, random

from ..lib import token

# 最初の通知する時間を設定するときに使用
TIME_LIST = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']

app = Flask(__name__)

line_bot_api = LineBotApi(token.CAT)
handler = WebhookHandler(token.CH)

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
    receive_text = event.message.text
    notify_hangout_laundry = 0

    # TIME_LISTに入っている数字を受信したとき洗濯物を干す通知をする時間を設定。
    if receive_text in TIME_LIST:
        notify_hangout_laundry = receive_text
        notify_message = receive_text + "時で設定しました。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=notify_message)
        )

    # 毎日定時に水やりが必要な画像を送信
    dt_hour = dt_now.hour
    if dt_hour == notify_hangout_laundry:
        send_image = image_url['seedling']
        # 画像を送信
        line_bot_api.broadcast(ImageSendMessage(
        original_content_url=send_image,
        preview_image_url=send_image
    ) )

    # 洗濯物を干したら水やりをしている画像を送信
    if '干した' in receive_text:
        send_image = image_url['watering']
        line_bot_api.broadcast(ImageSendMessage(
            original_content_url=send_image,
            preview_image_url=send_image
        ) )


    if '取り込んだ' in receive_text:

        if dt_h <= estimated_time+3:
            # 季節と確率で送る画像を選ぶ
            random_value = random.uniform(0, 10)

            if season == 2:
                if random_value <= 2:
                    send_image = image_url['cherry_blossoms']
                else:
                    send_image = image_url['dandelions']
            elif season == 3:
                if random_value <= 2:
                    send_image = image_url['sunflower']
                else:
                    send_image = image_url['hydrangea']
            elif season == 4:
                if random_value <= 2:
                    send_image = image_url['dianthus']
                else:
                    send_image = image_url['cosmos']
            else:
                if random_value <= 2:
                    send_image = image_url['christmas_rose']
                else:
                    send_image = image_url['cyclamen']
        else:
            # 洗濯物を取り込む時間を過ぎたら枯れた花を送信
            send_image = image_url['withered_flower']

        # 画像を送信
        line_bot_api.broadcast(ImageSendMessage(
            original_content_url=send_image,
            preview_image_url=send_image
        ) )

    # オウム返し部分
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
