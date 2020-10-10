import os
import redis
import query_string
from flask import Flask
from dotenv import load_dotenv
from linebot.models import TextSendMessage, TemplateSendMessage, ConfirmTemplate, PostbackAction, MessageAction

# start app
app = Flask(__name__)
load_dotenv(os.path.join(os.getcwd(), '.env'))

# Init Redis
redis_url = os.getenv('REDIS_URL')
r = redis.from_url(redis_url, decode_responses = True, charset = 'UTF-8')


def handle(event, line_bot_api):
    user_profile = line_bot_api.get_profile(event.source.user_id)
    app.logger.info("User [" + user_profile.user_id + "] has send message: " + event.message.text)
    user_id = user_profile.user_id
    user_status = r.get(user_id + ':status')

    if user_status:
        if user_status == 'followed':  # 若用戶現在的狀態是「剛追蹤」
            confirm_name(event, line_bot_api, user_status)


def confirm_name(event, line_bot_api, user_status):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '請確認姓名',
            template = ConfirmTemplate(
                text = '您的姓名是 [' + event.message.text + '] 嗎？',
                actions = [
                    PostbackAction(
                        label = '是',
                        display_text = '是',
                        data = 'action=yes&status=' + user_status
                    ),
                    PostbackAction(
                        label = '否',
                        display_text = '否',
                        data = 'action=no&status=' + user_status
                    )
                ]
            )
        )
    )
