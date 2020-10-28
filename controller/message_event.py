import os
import redis
from flask import Flask
from dotenv import load_dotenv
from linebot.models import TextSendMessage

from messages.crm import confirm_phone, confirm_name, confirm_birth_day, confirm_birth_time
from messages.general import send_message
from messages.service_2 import fate_num_result
from helper import utils

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
    user_name = r.get(channel_id + user_id + ':name')
    user_status = r.get(channel_id+user_id + ':status')
    user_action = r.get(channel_id+user_id + ':action')
    message = None

    log = "User {user}  send message: {message}"\
        .format(user = {'id': user_id, 'name': user_name, 'status': user_status, 'action': user_action}, message = event.message.text)
    app.logger.info(log)

    if event.message.text == 'st':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = user_status)
        )

    if event.message.text == 'cr':
        # delete redis which key prefix is current channel_id
        for key in r.scan_iter(channel_id + "*"):
            r.delete(key)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = 'delete redis cache')
        )

    if event.message.text == 'rf':
        utils.refresh_line_message(channel_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = 'refresh redis cache')
        )

    if user_status:
        # users data collecting
        if user_status == 'input_name':
            message = confirm_name(channel_id, event.message.text)
            r.set(channel_id+user_id + ':status', 'confirm_name')
        if user_status == 'input_birth_day':
            message = confirm_birth_day(channel_id, event.message.text)
            r.set(channel_id+user_id + ':status', 'confirm_birth_day')
        if user_status == 'input_birth_time':
            message = confirm_birth_time(channel_id, event.message.text)
            r.set(channel_id+user_id + ':status', 'confirm_birth_time')

        # services
        if user_action == 'input_fate_num':
            # TODO: 找貴人功能: 輸入了命盤編號後，要依照命盤編號找出對應的人的生辰時日，再計算彼此向性
            message = fate_num_result(channel_id, user_name)
            r.delete(channel_id+user_id + ':action')
        if user_action == 'input_phone':
            message = confirm_phone(channel_id, event.message.text)

        send_message(event, line_bot_api, message)
