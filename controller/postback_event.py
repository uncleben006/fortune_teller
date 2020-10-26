import os
import redis
import query_string
from flask import Flask
from dotenv import load_dotenv
from linebot.models import TextSendMessage

from controller.crm import confirm_gender, confirm_user_info
from controller.service_1 import love_fate_result, wealth_fate_result, service_1_menu
from controller.service_2 import ask_instructions, service_2_menu
from controller.service_3 import service_3_menu, line_booking, confirm_book_time, booking_result
from controller.service_4 import return_fate_num, service_4_menu
from controller.template import main_menu_template
from helper import utils

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
    channel_id = r.get(user_id + ':channel_id')

    app.logger.info("User [" + user_id + "] postback message: " + str(postback))
    user_status = r.get(channel_id + user_id + ':status')

    if user_status:

        if 'status' in postback:
            if postback['status'] == 'confirm_gender':
                user_status = 'confirm_gender'

        if user_status == 'confirm_name' and postback['action'] == 'confirm_name':

            if postback['reply'] == 'yes':
                confirm_gender(event, line_bot_api, channel_id)
                r.set(channel_id + user_id + ':status', 'confirm_gender')
                r.set(channel_id + user_id + ':name', postback['name'])

            if postback['reply'] == 'no':
                previous_status_text = utils.get_line_message(channel_id, 'welcome_text_second')
                reply_text_message(event, line_bot_api, previous_status_text)
                r.set(channel_id + user_id + ':status', 'input_name')

        if user_status == 'confirm_gender' and postback['action'] == 'confirm_gender':
            user_name = r.get(channel_id + user_id + ':name')
            next_status_text = utils.get_line_message(channel_id, 'input_birth_day').format(name=user_name)
            reply_text_message(event, line_bot_api, next_status_text)
            r.set(channel_id + user_id + ':status', 'input_birth_day')
            r.set(channel_id + user_id + ':gender', postback['reply'])

        if user_status == 'confirm_birth_day' and postback['action'] == 'confirm_birth_day':

            if postback['reply'] == 'yes':
                next_status_text = utils.get_line_message(channel_id, 'input_birth_time')
                reply_text_message(event, line_bot_api, next_status_text)
                r.set(channel_id + user_id + ':status', 'input_birth_time')
                r.set(channel_id + user_id + ':birth_day', postback['birth_day'])
            if postback['reply'] == 'no':
                user_name = r.get(channel_id + user_id + ':name')
                previous_status_text = utils.get_line_message(channel_id, 'input_birth_day').format(name=user_name)
                reply_text_message(event, line_bot_api, previous_status_text)
                r.set(channel_id + user_id + ':status', 'input_birth_day')

        if user_status == 'confirm_birth_time' and postback['action'] == 'confirm_birth_time':

            if postback['reply'] == 'yes':
                user_name = r.get(channel_id + user_id + ':name')
                user_gender = r.get(channel_id + user_id + ':gender')
                user_gender = {'female': '女', 'male': '男'}[user_gender]
                user_birth_day = r.get(channel_id + user_id + ':birth_day')
                user_birth_time = postback['birth_time']

                confirm_user_info(event, line_bot_api, channel_id, user_name, user_gender, user_birth_day,
                                  user_birth_time)

                r.set(channel_id + user_id + ':status', 'confirm_user_info')
                r.set(channel_id + user_id + ':birth_time', postback['birth_time'])

            if postback['reply'] == 'no':
                previous_status_text = utils.get_line_message(channel_id, 'input_birth_time')
                reply_text_message(event, line_bot_api, previous_status_text)
                r.set(channel_id + user_id + ':status', 'input_birth_time')

        if user_status == 'confirm_user_info' and postback['action'] == 'confirm_user_info':

            if postback['reply'] == 'yes':
                r.set(channel_id + user_id + ':status', 'contacted')

                channel_id = r.get(user_id + ':channel_id')
                user_name = r.get(channel_id + user_id + ':name')
                user_gender = r.get(channel_id + user_id + ':gender')
                user_birth_day = r.get(channel_id + user_id + ':birth_day')
                user_birth_time = r.get(channel_id + user_id + ':birth_time')

                show_menu(event, line_bot_api, user_name)

                # Store user info after complete the first stage of the info collection
                utils.store_user_info(channel_id, user_id, user_name, user_gender,
                                      user_birth_day, user_birth_time, 'contacted')

            if postback['reply'] == 'no':
                previous_status_text = utils.get_line_message(channel_id, 'welcome_text_second')
                reply_text_message(event, line_bot_api, previous_status_text)
                r.set(channel_id + user_id + ':status', 'input_name')

        if user_status == 'contacted' and postback['action'] == 'show_menu':
            user_name = r.get(channel_id + user_id + ':name')
            show_menu(event, line_bot_api, user_name)

        if user_status == 'contacted' and postback['action'] == 'service_1':
            app.logger.info('service_1')
            service_1_menu(event, line_bot_api)

        if user_status == 'contacted' and postback['action'] == 'wealth_fate':
            app.logger.info('wealth_fate')
            user_name = r.get(channel_id + user_id + ':name')
            wealth_fate_result(event, line_bot_api, user_name)

        if user_status == 'contacted' and postback['action'] == 'love_fate':
            app.logger.info('love_fate')
            user_name = r.get(channel_id + user_id + ':name')
            love_fate_result(event, line_bot_api, user_name)

        if user_status == 'contacted' and postback['action'] == 'service_2':
            app.logger.info('service_2')
            service_2_menu(event, line_bot_api)

        if user_status == 'contacted' and postback['action'] == 'input_fate_num':
            app.logger.info('input_fate_num')
            text = '請輸入對方的命盤編號。'
            reply_text_message(event, line_bot_api, text)
            r.set(channel_id + user_id + ':action', 'input_fate_num')

        if user_status == 'contacted' and postback['action'] == 'ask_instructions':
            app.logger.info('ask_instructions')
            ask_instructions(event, line_bot_api)

        if user_status == 'contacted' and postback['action'] == 'service_3':
            app.logger.info('service_3')
            service_3_menu(event, line_bot_api)

        if user_status == 'contacted' and postback['action'] == 'line_booking':
            app.logger.info('line_booking')
            line_booking(event, line_bot_api)

        if user_status == 'contacted' and postback['action'] == 'book_time':
            app.logger.info('book_time')
            r.set(channel_id + user_id + ':date', postback['date'])
            r.set(channel_id + user_id + ':weekday', postback['weekday'])
            r.set(channel_id + user_id + ':time', postback['time'])
            book_date = postback['date']
            weekday = postback['weekday']
            time = postback['time']
            confirm_book_time(event, line_bot_api, book_date, weekday, time)

        if user_status == 'contacted' and postback['action'] == 'confirm_book_time':
            app.logger.info('confirm_book_time')
            user_name = r.get(channel_id + user_id + ':name')

            if postback['reply'] == 'yes':
                text = '['+user_name+'] 您好，請輸入您的電話號碼'
                reply_text_message(event, line_bot_api, text)
                r.set(channel_id + user_id + ':action', 'input_phone')
            if postback['reply'] == 'no':
                show_menu(event, line_bot_api, user_name)

        if user_status == 'contacted' and postback['action'] == 'confirm_phone':
            app.logger.info('confirm_phone')
            user_name = r.get(channel_id + user_id + ':name')

            if postback['reply'] == 'yes':
                phone = postback['phone']
                book_date = r.get(channel_id + user_id + ':date')
                weekday = r.get(channel_id + user_id + ':weekday')
                time = r.get(channel_id + user_id + ':time')

                booking_result(event, line_bot_api, user_name, phone, book_date, weekday, time)
                r.delete(channel_id + user_id + ':action')
                # TODO: 結束預約流程後，要把使用者的預約資訊存入 postgreSQL

            if postback['reply'] == 'no':
                text = '[' + user_name + '] 您好，請輸入您的電話號碼'
                reply_text_message(event, line_bot_api, text)
                r.set(channel_id + user_id + ':action', 'input_phone')

        if user_status == 'contacted' and postback['action'] == 'service_4':
            app.logger.info('service_4')
            service_4_menu(event, line_bot_api)

        if user_status == 'contacted' and postback['action'] == 'query_fate_num':
            app.logger.info('query_fate_num')
            # TODO: 用 user_id 跟 channel_id query 出 fate_num
            return_fate_num(event, line_bot_api)


def reply_text_message(event, line_bot_api, text):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = text)
    )


def show_menu(event, line_bot_api, user_name):
    line_bot_api.reply_message(
        event.reply_token,
        main_menu_template(user_name)
    )
