import os
import redis
from flask import Flask
from dotenv import load_dotenv
from linebot.models import ImageSendMessage, TextSendMessage

from controller.postback_event import show_menu
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
    if not utils.is_user(user_id):
        line_bot_api.reply_message(
            event.reply_token,
            [
                ImageSendMessage(
                    original_content_url = 'https://yt3.ggpht.com/-jHaW03KgtAc/AAAAAAAAAAI/AAAAAAAAAAA/9EFyOq-T5Ts/s900-c-k-no/photo.jpg',
                    preview_image_url = 'https://yt3.ggpht.com/-jHaW03KgtAc/AAAAAAAAAAI/AAAAAAAAAAA/9EFyOq-T5Ts/s900-c-k-no/photo.jpg'
                ),
                TextSendMessage(text = '歡迎來到「唐綺陽運勢所」，我們將提供您的運勢預報'),
                TextSendMessage(text = '請輸入您的姓名'),
            ]
        )

        # use redis to update user status
        r.set(user_id + ':status', 'input_name')

    else:
        # Show the menu if user is exist in database.
        user_name = r.get(user_id + ':name')
        if not user_name:
            user_data = utils.get_user(user_id)
            r.set(user_id + ':channel_id', user_data[0])
            r.set(user_id + ':name', user_data[2])
            r.set(user_id + ':gender',user_data[3])
            r.set(user_id + ':birth_day',user_data[4])
            r.set(user_id + ':birth_time',user_data[5])
            r.set(user_id + ':status',user_data[6])
            user_name = user_data[2]
        show_menu(event, line_bot_api, user_name)
