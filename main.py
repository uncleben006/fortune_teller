import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# flask
from flask import Flask, request, abort

# line sdk
from linebot import (LineBotApi, WebhookHandler, WebhookParser)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, FollowEvent)

# custom module
from controller import follow_event, message_event
from helper.utils import get_channel

# start app
app = Flask(__name__)
load_dotenv(os.path.join(os.getcwd(), '.env'))

# Line bot config
line_bot_api = LineBotApi('channel_access_token')
handler = WebhookHandler('channel_secret')

# log config
logging.basicConfig(filename = 'var/access.log',
                    level = logging.DEBUG,
                    format = '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# log example
# app.logger.error("Something has gone very wrong")
# app.logger.warning("You've been warned")
# app.logger.info("Here's some info")
# app.logger.debug("Meaningless debug information")


@app.route('/', methods = ['GET'])
def index_html():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return '<h1>歡迎來到命理師 line bot</h1><br>現在時間' + dt_string


@app.route("/callback/<channel_id>", methods = ['POST'])
def callback(channel_id):
    global line_bot_api
    global handler

    # Query channel information using channel_id
    app.logger.info("Channel_id from Webhook: " + channel_id)
    channel_secret, channel_access_token = get_channel(channel_id)

    # start up line_bot_api and handler
    line_bot_api = LineBotApi(channel_access_token)
    handler.parser = WebhookParser(channel_secret)

    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text = True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
        print(handler)

    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message = TextMessage)
def handle_message(event):
    message_event.handle(event, line_bot_api)


@handler.add(FollowEvent)
def handle_follow(event):
    follow_event.handle(event, line_bot_api)


if __name__ == "__main__":
    app.run()
