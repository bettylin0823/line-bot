from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('bCQSqWuky5IORUhmIKyuDqkXYnQcrhEBC5BM9qZgb8g7rkpmPIUCtWk3wda8knU5GIVsbfiadQyG52w74VH33+XFlgmHu9AYXHXIqk+0fRqdBmmc1Fu+i9of3Pj4NbHrv2pu9e+f6g57ta4Mn9x46gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ee61ced4b3361c43fb0567af08f78a87')


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
    msg = event.message.text
    r = 'Sorry, can you repeat again?'

    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

    if msg in ['hi', 'Hi']:
        r = 'hi'
    elif msg == '你吃飯了沒':
        r = '還沒'
    elif msg == '你是誰':
        r = 'I am your robot. Ready for serving.'
    elif '訂位' in msg:
        r = 'You wanna order, right?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()