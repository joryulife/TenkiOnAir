import json
from flask import Flask, request, abort
from MysqlManager import MysqlConnectorManager

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

sqladdmin = open('../lib/sqladdmin.json','r')
sqladdmin = json.load(sqladdmin)
CM = MysqlConnectorManager(user=sqladdmin['user'],
    password=sqladdmin['password'],
    host=sqladdmin['host'],
    database_name=sqladdmin['database'])
CM.start_connection()
#q = ("insert into TESTTABLE value(%s,%s)")
#ps =(2, 'TEST2')
#ans =CM.insert_contents(q,ps)
#print(ans)

app = Flask(__name__)

line_bot_api = LineBotApi(token["CAT"])
handler = WebhookHandler(token["CH"])

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
    print(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
