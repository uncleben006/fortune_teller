import os
import redis
from flask import Flask
from dotenv import load_dotenv
from linebot.models import ImageSendMessage, TextSendMessage
from helper.utils import is_user

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
    if not is_user(user_id):
        line_bot_api.reply_message(
            event.reply_token,
            [
                ImageSendMessage(
                    original_content_url = 'https://yt3.ggpht.com/-jHaW03KgtAc/AAAAAAAAAAI/AAAAAAAAAAA/9EFyOq-T5Ts/s900-c-k-no/photo.jpg',
                    preview_image_url = 'https://yt3.ggpht.com/-jHaW03KgtAc/AAAAAAAAAAI/AAAAAAAAAAA/9EFyOq-T5Ts/s900-c-k-no/photo.jpg'
                ),
                TextSendMessage(text = '[客製] - 歡迎來到「唐綺陽運勢所」，我們將提供您的運勢預報'),
                TextSendMessage(text = '[客製] - 請輸入您的姓名'),
            ]
        )

        # use redis to update user status
        r.set(user_id + ':status', 'input_name')

    else:
        # TODO: 如果 user_id 已經存在於資料庫中，則直接取出其名稱並顯示歡迎訊息
        line_bot_api.reply_message(
            event.reply_token,
            [
                ImageSendMessage(
                    original_content_url = 'https://yt3.ggpht.com/-jHaW03KgtAc/AAAAAAAAAAI/AAAAAAAAAAA/9EFyOq-T5Ts/s900-c-k-no/photo.jpg',
                    preview_image_url = 'https://yt3.ggpht.com/-jHaW03KgtAc/AAAAAAAAAAI/AAAAAAAAAAA/9EFyOq-T5Ts/s900-c-k-no/photo.jpg'
                ),
                TextSendMessage(text = '[客製] - 您好，好久不見'),
            ]
        )
