from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from dotenv import load_dotenv
from datetime import datetime
import psycopg2
import os
import json
import logging

# load env file
load_dotenv(os.path.join(os.getcwd(), '.env'))

app = Flask(__name__)

# Line bot config
line_bot_api = LineBotApi('channel_access_token')
handler = WebhookHandler('channel_secret')
channel_email = None

# log config
logging.basicConfig(filename='var/access.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

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
    global channel_email

    # Query channel information using channel_id
    app.logger.info("Channel_id from Webhook: " + channel_id)
    result = get_channel(channel_id)
    channel_email = result[0]
    channel_secret = result[1]
    channel_access_token = result[2]

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


# Query channel information using channel_id
def get_channel(channel_id):
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    sql = "SELECT email, secret, access_token FROM channel WHERE channel.id = '%s' " % channel_id
    app.logger.info("Start query channel: " + sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    app.logger.info("Result: " + json.dumps(result))
    cursor.close()
    conn.close()
    return result


@handler.add(MessageEvent, message = TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = event.message.text))


if __name__ == "__main__":
    app.run()
