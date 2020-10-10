import os
import redis
import query_string
from flask import Flask
from dotenv import load_dotenv
from linebot.models import TextSendMessage

# start app
app = Flask(__name__)
load_dotenv(os.path.join(os.getcwd(), '.env'))

# Init Redis
redis_url = os.getenv('REDIS_URL')
r = redis.from_url(redis_url, decode_responses = True, charset = 'UTF-8')


def handle(event, line_bot_api):
    postback = query_string.parse(event.postback.data)
    user_profile = line_bot_api.get_profile(event.source.user_id)
    user_id = user_profile.user_id
    app.logger.info("User [" + user_id + "] postback message: " + str(postback))
    user_status = r.get(user_id + ':status')

    if user_status:
        if user_status == 'confirm_name' and postback['action'] == 'confirm_name':
            if postback['reply'] == 'yes':
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text = '[客製] - ['+postback['name']+'] 您好,請填寫您的國曆生日。  如1979年8月30日。請打19790830。')
                )
                r.set(user_id + ':status', 'input_birthday')
            if postback['reply'] == 'no':
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text = '[客製] - 請輸入您的姓名')
                )
                r.set(user_id + ':status', 'followed')


