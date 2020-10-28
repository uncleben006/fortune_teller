import os
import redis
import query_string
from flask import Flask
from dotenv import load_dotenv
from linebot.models import TextSendMessage

from messages.crm import confirm_gender, confirm_user_info, input_birth_day, input_birth_time
from messages.general import send_message, main_menu_template
from messages.service_1 import love_fate, wealth_fate, service_1_menu_template
from messages.service_2 import service_2_instructions, service_2_menu_template
from messages.service_3 import service_3_menu, confirm_book_time, booking_result, line_booking_template, input_phone
from messages.service_4 import return_fate_num, service_4_menu_template
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
    user_name = r.get(channel_id + user_id + ':name')
    user_status = r.get(channel_id + user_id + ':status')
    message = None

    log = "User {user}  postback message: {postback}"\
        .format(user = {'id': user_id, 'name': user_name, 'status': user_status}, postback = str(postback))
    app.logger.info(log)

    if user_status:

        if postback['action'] == 'confirm_gender':
            user_status = 'confirm_gender'
            postback['reply'] = r.get(channel_id + user_id + ':gender')

        if user_status == 'confirm_name' and postback['action'] == 'confirm_name':

            if postback['reply'] == 'yes':
                confirm_gender(event, line_bot_api, channel_id)
                r.set(channel_id + user_id + ':status', 'confirm_gender')
                r.set(channel_id + user_id + ':name', postback['name'])

            if postback['reply'] == 'no':
                message = TextSendMessage(text = utils.get_line_message(channel_id, 'welcome_text_second'))
                r.set(channel_id + user_id + ':status', 'input_name')

        if user_status == 'confirm_gender' and postback['action'] == 'confirm_gender':
            input_birth_day(event, line_bot_api, channel_id, user_name)
            r.set(channel_id + user_id + ':status', 'input_birth_day')
            r.set(channel_id + user_id + ':gender', postback['reply'])

        if user_status == 'confirm_birth_day' and postback['action'] == 'confirm_birth_day':

            if postback['reply'] == 'yes':
                input_birth_time(event, line_bot_api, channel_id)
                r.set(channel_id + user_id + ':status', 'input_birth_time')
                r.set(channel_id + user_id + ':birth_day', postback['birth_day'])
            if postback['reply'] == 'no':
                input_birth_day(event, line_bot_api, channel_id, user_name)
                r.set(channel_id + user_id + ':status', 'input_birth_day')

        if user_status == 'confirm_birth_time' and postback['action'] == 'confirm_birth_time':

            if postback['reply'] == 'yes':
                user_gender = r.get(channel_id + user_id + ':gender')
                user_gender = {'female': '女', 'male': '男'}[user_gender]
                user_birth_day = r.get(channel_id + user_id + ':birth_day')
                user_birth_time = postback['birth_time']

                confirm_user_info(event, line_bot_api, channel_id,
                                  user_name, user_gender, user_birth_day, user_birth_time)

                r.set(channel_id + user_id + ':status', 'confirm_user_info')
                r.set(channel_id + user_id + ':birth_time', postback['birth_time'])

            if postback['reply'] == 'no':
                input_birth_time(event, line_bot_api, channel_id)
                r.set(channel_id + user_id + ':status', 'input_birth_time')

        if user_status == 'confirm_user_info' and postback['action'] == 'confirm_user_info':

            if postback['reply'] == 'yes':
                r.set(channel_id + user_id + ':status', 'contacted')

                user_gender = r.get(channel_id + user_id + ':gender')
                user_birth_day = r.get(channel_id + user_id + ':birth_day')
                user_birth_time = r.get(channel_id + user_id + ':birth_time')

                message = main_menu_template(channel_id, user_name)

                # Store user info after complete the first stage of the info collection
                utils.store_user_info(channel_id, user_id, user_name, user_gender,
                                      user_birth_day, user_birth_time, 'contacted')

            if postback['reply'] == 'no':
                message = TextSendMessage(text = utils.get_line_message(channel_id, 'welcome_text_second'))
                r.set(channel_id + user_id + ':status', 'input_name')

        if user_status == 'contacted' and postback['action'] == 'show_menu':
            message = main_menu_template(channel_id, user_name)

        if user_status == 'contacted' and postback['action'] == 'service_1':
            message = service_1_menu_template(channel_id, user_name)

        if user_status == 'contacted' and postback['action'] == 'wealth_fate':
            message = wealth_fate(channel_id, user_name)

        if user_status == 'contacted' and postback['action'] == 'love_fate':
            message = love_fate(channel_id, user_name)

        if user_status == 'contacted' and postback['action'] == 'service_2':
            message = service_2_menu_template(channel_id, user_name)

        # TODO: 找貴人功能: 輸入了命盤編號後，要依照命盤編號找出對應的人的生辰時日，再計算彼此向性
        if user_status == 'contacted' and postback['action'] == 'input_fate_num':
            message = TextSendMessage(text = utils.get_line_message(channel_id, 'input_fate_num'))
            r.set(channel_id + user_id + ':action', 'input_fate_num')

        if user_status == 'contacted' and postback['action'] == 'ask_instructions':
            message = service_2_instructions(channel_id, user_name)

        if user_status == 'contacted' and postback['action'] == 'service_3':
            message = service_3_menu(channel_id, user_name)

        if user_status == 'contacted' and postback['action'] == 'line_booking':
            message = line_booking_template()

        if user_status == 'contacted' and postback['action'] == 'book_time':
            book_date, weekday, time = postback['date'], postback['weekday'], postback['time']
            message = confirm_book_time(book_date, weekday, time)
            r.set(channel_id + user_id + ':date', book_date)
            r.set(channel_id + user_id + ':weekday', weekday)
            r.set(channel_id + user_id + ':time', time)

        if user_status == 'contacted' and postback['action'] == 'confirm_book_time':
            if postback['reply'] == 'yes':
                message = input_phone(channel_id, user_name)
                r.set(channel_id + user_id + ':action', 'input_phone')
            if postback['reply'] == 'no':
                message = main_menu_template(channel_id, user_name)

        if user_status == 'contacted' and postback['action'] == 'confirm_phone':

            if postback['reply'] == 'yes':
                phone = postback['phone']
                book_date = r.get(channel_id + user_id + ':date')
                weekday = r.get(channel_id + user_id + ':weekday')
                time = r.get(channel_id + user_id + ':time')

                message = booking_result(channel_id, user_name, phone, book_date, weekday, time)
                r.delete(channel_id + user_id + ':action')
                # TODO: 結束預約流程後，要把使用者的預約資訊存入 postgreSQL

            if postback['reply'] == 'no':
                message = input_phone(channel_id, user_name)
                r.set(channel_id + user_id + ':action', 'input_phone')

        if user_status == 'contacted' and postback['action'] == 'service_4':
            message = service_4_menu_template(channel_id)

        if user_status == 'contacted' and postback['action'] == 'query_fate_num':
            # TODO: 查詢命盤編號: 用 user_id 跟 channel_id 找出 fate_num
            message = return_fate_num(channel_id)

    send_message(event, line_bot_api, message)
