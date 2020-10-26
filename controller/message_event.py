import os
import redis
from flask import Flask
from dotenv import load_dotenv
from linebot.models import TextSendMessage

from controller.crm import confirm_phone, confirm_name, confirm_birth_day, confirm_birth_time
from controller.service_2 import fate_num_result

# start app
app = Flask(__name__)
load_dotenv(os.path.join(os.getcwd(), '.env'))

# Init Redis
redis_url = os.getenv('REDIS_URL')
r = redis.from_url(redis_url, decode_responses = True, charset = 'UTF-8')


def handle(event, line_bot_api):
    user_profile = line_bot_api.get_profile(event.source.user_id)
    user_id = user_profile.user_id
    channel_id = r.get(user_id + ':channel_id')

    app.logger.info("User [" + user_id + "] has send message: " + event.message.text)
    user_status = r.get(channel_id+user_id + ':status')
    user_action = r.get(channel_id+user_id + ':action')

    if event.message.text == 'status':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = user_status)
        )

    if event.message.text == 'clear':
        # delete redis which key prefix is current channel_id
        for key in r.scan_iter(channel_id + "*"):
            r.delete(key)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = 'delete redis cache')
        )

    if user_status:
        # users data collecting
        if user_status == 'input_name':
            confirm_name(event, line_bot_api, channel_id)
            r.set(channel_id+user_id + ':status', 'confirm_name')
        if user_status == 'input_birth_day':
            confirm_birth_day(event, line_bot_api, channel_id)
            r.set(channel_id+user_id + ':status', 'confirm_birth_day')
        if user_status == 'input_birth_time':
            confirm_birth_time(event, line_bot_api, channel_id)
            r.set(channel_id+user_id + ':status', 'confirm_birth_time')

        # services
        if user_action == 'input_fate_num':
            # TODO: 這邊要加一段，用 fate number (命盤編號) 來 query 使用者資料的 SQL
            app.logger.info('Fate num:' + event.message.text)
            user_name = r.get(channel_id + user_id + ':name')
            fate_num_result(event, line_bot_api, user_name)
            r.delete(channel_id+user_id + ':action')
        if user_action == 'input_phone':
            app.logger.info('Phone num:' + event.message.text)
            confirm_phone(event, line_bot_api, channel_id)
