import os
import redis
from flask import Flask
from dotenv import load_dotenv
from linebot.models import ImageSendMessage, TextSendMessage

from controller.postback_event import show_menu
from controller.template import welcome_text
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
                ImageSendMessage(
                    original_content_url = 'https://destiny.quanzar.com.tw/wp-content/uploads/2020/09/fortune-teller_01_small.png',
                    preview_image_url = 'https://destiny.quanzar.com.tw/wp-content/uploads/2020/09/fortune-teller_01_small.png'
                ),
                TextSendMessage(text = welcome_text()),
                TextSendMessage(text = '請輸入您的姓名'),
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
        show_menu(event, line_bot_api, user_name)
