import os
import redis
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
    user_id = user_profile.user_id
    app.logger.info("User [" + user_id + "] has send message: " + event.message.text)
    user_status = r.get(user_id + ':status')

    if event.message.text == 'status':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = user_status)
        )

    if user_status:
        if user_status == 'input_name':
            confirm_name(event, line_bot_api)
            r.set(user_id + ':status', 'confirm_name')
        if user_status == 'input_birthday':
            confirm_birthday(event, line_bot_api)
            r.set(user_id + ':status', 'confirm_birthday')


def confirm_birthday(event, line_bot_api):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '請確認國曆生日',
            template = ConfirmTemplate(
                text = '您的國曆生日為 ' + event.message.text[:4] + '年' + event.message.text[4:6] + '月' + event.message.text[
                                                                                                   -2:] + '日 嗎？',
                actions = [
                    PostbackAction(
                        label = '是',
                        display_text = '是',
                        data = 'action=confirm_birthday&reply=yes&name=' + event.message.text
                    ),
                    PostbackAction(
                        label = '否',
                        display_text = '否',
                        data = 'action=confirm_birthday&reply=no'
                    )
                ]
            )
        )
    )


def confirm_name(event, line_bot_api):
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
                        data = 'action=confirm_name&reply=yes&name=' + event.message.text
                    ),
                    PostbackAction(
                        label = '否',
                        display_text = '否',
                        data = 'action=confirm_name&reply=no'
                    )
                ]
            )
        )
    )
