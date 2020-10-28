import os
import redis
from flask import Flask
from dotenv import load_dotenv
from linebot.models import ImageSendMessage, TextSendMessage

from controller.general import main_menu_template, send_message
from helper import utils

# start app
app = Flask(__name__)
load_dotenv(os.path.join(os.getcwd(), '.env'))

# Init Redis
redis_url = os.getenv('REDIS_URL')
r = redis.from_url(redis_url, decode_responses = True, charset = 'UTF-8')


def handle(event, line_bot_api):
    # get user info
    user_profile = line_bot_api.get_profile(event.source.user_id)
    app.logger.info("A user has followed: " + str(user_profile))
    user_id = user_profile.user_id
    channel_id = r.get(user_id + ':channel_id')

    # if user not exist in db, start collect user info
    if not utils.is_user(user_id, channel_id):
        line_bot_api.reply_message(
            event.reply_token,
            [
                # 從 redis 拿 message，若沒有則從 DB 搜尋全部並且存進 redis ( channel_id+context_id => message)
                ImageSendMessage(
                    original_content_url = utils.get_line_message(channel_id, 'welcome_image'),
                    preview_image_url = utils.get_line_message(channel_id, 'welcome_image')
                ),
                TextSendMessage(text = utils.get_line_message(channel_id, 'welcome_text_first')),
                TextSendMessage(text = utils.get_line_message(channel_id, 'welcome_text_second')),
            ]
        )

        # use redis to update user status
        r.set(channel_id+user_id + ':status', 'input_name')

    # else get the user info and set in redis
    else:
        user_data = utils.get_user(user_id, channel_id)
        r.set(user_id + ':channel_id', user_data[0])
        r.set(channel_id+user_id + ':name', user_data[2])
        r.set(channel_id+user_id + ':gender', user_data[3])
        r.set(channel_id+user_id + ':birth_day', user_data[4])
        r.set(channel_id+user_id + ':birth_time', user_data[5])
        r.set(channel_id+user_id + ':status', user_data[6])
        user_name = user_data[2]

        message = main_menu_template(channel_id, user_name)
        send_message(event, line_bot_api, message)
