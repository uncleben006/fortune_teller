import os
import redis
import query_string
from flask import Flask
from datetime import date
from dotenv import load_dotenv
from linebot.models import TextSendMessage, TemplateSendMessage, ConfirmTemplate, PostbackAction, ButtonsTemplate
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
    app.logger.info("User [" + user_id + "] postback message: " + str(postback))
    user_status = r.get(user_id + ':status')

    if user_status:

        if user_status == 'confirm_name' and postback['action'] == 'confirm_name':

            if postback['reply'] == 'yes':
                confirm_gender(event, line_bot_api)
                r.set(user_id + ':status', 'confirm_gender')
                r.set(user_id + ':name', postback['name'])

            if postback['reply'] == 'no':
                previous_status_text = '請輸入您的姓名'
                reply_text_message(event, line_bot_api, previous_status_text)
                r.set(user_id + ':status', 'input_name')

        if user_status == 'confirm_gender' and postback['action'] == 'confirm_gender':
            user_name = r.get(user_id + ':name')
            next_status_text = '[' + user_name + '] 您好,請填寫您的國曆生日。 如1979年8月30日。請打19790830。'
            reply_text_message(event, line_bot_api, next_status_text)
            r.set(user_id + ':status', 'input_birth_day')
            r.set(user_id + ':gender', postback['reply'])

        if user_status == 'confirm_birth_day' and postback['action'] == 'confirm_birth_day':

            if postback['reply'] == 'yes':
                next_status_text = '請填寫您的出生時間。 例如晚上 11：30，請打23:30。'
                reply_text_message(event, line_bot_api, next_status_text)
                r.set(user_id + ':status', 'input_birth_time')
                r.set(user_id + ':birth_day', postback['birth_day'])
            if postback['reply'] == 'no':
                user_name = r.get(user_id + ':name')
                previous_status_text = '[' + user_name + '] 您好,請填寫您的國曆生日。 如1979年8月30日。請打19790830。'
                reply_text_message(event, line_bot_api, previous_status_text)
                r.set(user_id + ':status', 'input_birth_day')

        if user_status == 'confirm_birth_time' and postback['action'] == 'confirm_birth_time':

            if postback['reply'] == 'yes':
                confirm_user_info(event, line_bot_api, postback, user_id)
                r.set(user_id + ':status', 'confirm_user_info')
                r.set(user_id + ':birth_time', postback['birth_time'])
            if postback['reply'] == 'no':
                previous_status_text = '請填寫您的出生時間。 例如晚上 11：30，請打23:30。'
                reply_text_message(event, line_bot_api, previous_status_text)
                r.set(user_id + ':status', 'input_birth_time')

        if user_status == 'confirm_user_info' and postback['action'] == 'confirm_user_info':

            if postback['reply'] == 'yes':
                r.set(user_id + ':status', 'contacted')

                channel_id = r.get(user_id + ':channel_id')
                user_name = r.get(user_id + ':name')
                user_gender = r.get(user_id + ':gender')
                user_birth_day = r.get(user_id + ':birth_day')
                user_birth_time = r.get(user_id + ':birth_time')

                show_menu(event, line_bot_api, user_name)

                # Store user info after complete the first stage of the info collection
                utils.store_user_info(channel_id, user_id, user_name, user_gender, user_birth_day, user_birth_time, 'contacted')

            if postback['reply'] == 'no':
                previous_status_text = '請輸入您的姓名。'
                reply_text_message(event, line_bot_api, previous_status_text)
                r.set(user_id + ':status', 'input_name')

        if user_status == 'contacted' and postback['action'] == 'show_menu':
            user_name = r.get(user_id + ':name')
            show_menu(event, line_bot_api, user_name)
        if user_status == 'contacted' and postback['action'] == 'service_1':
            app.logger.info('service_1')
            service_1_menu(event, line_bot_api)
        if user_status == 'contacted' and postback['action'] == 'wealth_fate':
            app.logger.info('wealth_fate')
            user_name = r.get(user_id + ':name')
            wealth_fate_result(event, line_bot_api, user_name)
        if user_status == 'contacted' and postback['action'] == 'love_fate':
            app.logger.info('love_fate')
            user_name = r.get(user_id + ':name')
            love_fate_result(event, line_bot_api, user_name)

        if user_status == 'contacted' and postback['action'] == 'service_2':
            app.logger.info('service_2')
        if user_status == 'contacted' and postback['action'] == 'service_3':
            app.logger.info('service_3')
        if user_status == 'contacted' and postback['action'] == 'service_4':
            app.logger.info('service_4')


def love_fate_result(event, line_bot_api, user_name):
    today = date.today()
    text = '[' + user_name + '] ' + str(today.month) + '月' + str(today.day) +\
           '日愛情運勢\n\n' +\
           '今日愛情運勢：★★★★☆\n' +\
           '今日愛情數字：6\n' +\
           '今日愛情時間：09:00-10:00\n' +\
           '今日愛情顏色：水晶紫\n\n' +\
           '明日愛情運勢：★★★★★\n' +\
           '明日愛情數字：9\n' +\
           '明日愛情時間：19:00-20:00\n' +\
           '明日愛情顏色：湖水藍\n\n' +\
           '說明：顏色包含衣服、包包、鞋子、配件等皆可\n\n' +\
           '[ △△ 運命所 OO 老師關心您，過去 30 天有 20 天見到過您 ]'
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text = text),
            service_1_menu_template()
        ]
    )


def wealth_fate_result(event, line_bot_api, user_name):
    today = date.today()
    text = '[' + user_name + '] ' + str(today.month) + '月' + str(today.day) +\
           '日財運運勢\n\n' +\
           '今日財運運勢：★★★★☆\n' +\
           '今日財運數字：6\n' +\
           '今日財運時間：09:00-10:00\n' +\
           '今日財運顏色：水晶紫\n\n' +\
           '明日財運運勢：★★★★★\n' +\
           '明日財運數字：9\n' +\
           '明日財運時間：19:00-20:00\n' +\
           '明日財運顏色：湖水藍\n\n' +\
           '說明：顏色包含衣服、包包、鞋子、配件等皆可\n\n' +\
           '[ △△ 運命所 OO 老師關心您，過去 30 天有 20 天見到過您 ]'
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text = text),
            service_1_menu_template()
        ]
    )


def service_1_menu(event, line_bot_api):
    line_bot_api.reply_message(
        event.reply_token,
        service_1_menu_template()
    )


def service_1_menu_template():
    return TemplateSendMessage(
        alt_text = 'Buttons template',
        template = ButtonsTemplate(
            thumbnail_image_url = 'https://yt3.ggpht.com/-jHaW03KgtAc/AAAAAAAAAAI/AAAAAAAAAAA/9EFyOq-T5Ts/s900-c-k-no/photo.jpg',
            title = 'OO 老師 協助您提升運勢',
            text = '請選擇想要提升哪種運勢？',
            actions = [
                PostbackAction(
                    label = '提升財運運勢',
                    display_text = '提升財運運勢',
                    data = 'action=wealth_fate'
                ),
                PostbackAction(
                    label = '提升愛情運勢',
                    display_text = '提升愛情運勢',
                    data = 'action=love_fate'
                ),
                PostbackAction(
                    label = '回主選單',
                    display_text = '回主選單',
                    data = 'action=show_menu'
                ),
            ]
        )
    )


def reply_text_message(event, line_bot_api, previous_status_text):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = previous_status_text)
    )


def confirm_gender(event, line_bot_api):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '請確認性別',
            template = ConfirmTemplate(
                text = '您的性別為',
                actions = [
                    PostbackAction(
                        label = '男',
                        display_text = '男',
                        data = 'action=confirm_gender&reply=male'
                    ),
                    PostbackAction(
                        label = '女',
                        display_text = '女',
                        data = 'action=confirm_gender&reply=female'
                    )
                ]
            )
        )
    )


def confirm_user_info(event, line_bot_api, postback, user_id):
    user_name = r.get(user_id + ':name')
    user_gender = r.get(user_id + ':gender')
    user_gender = {'female': '女', 'male': '男'}[user_gender]
    user_birth_day = r.get(user_id + ':birth_day')
    user_birth_time = postback['birth_time']
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '確認所有資料',
            template = ConfirmTemplate(
                text = '您是 [' + user_name + '], ' + user_gender + '性, 生日為 ' +
                       user_birth_day[:4] + '/' + user_birth_day[4:6] + '/' + user_birth_day[-2:] +
                       ' ' + user_birth_time + ' ?',
                actions = [
                    PostbackAction(
                        label = '是',
                        display_text = '是',
                        data = 'action=confirm_user_info&reply=yes'
                    ),
                    PostbackAction(
                        label = '否',
                        display_text = '否',
                        data = 'action=confirm_user_info&reply=no'
                    )
                ]
            )
        )
    )


def show_menu(event, line_bot_api, user_name):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = 'Buttons template',
            template = ButtonsTemplate(
                thumbnail_image_url = 'https://yt3.ggpht.com/-jHaW03KgtAc/AAAAAAAAAAI/AAAAAAAAAAA/9EFyOq-T5Ts/s900-c-k-no/photo.jpg',
                title = '運命所 OO 老師',
                text = '提升 [' + user_name + '] 運勢服務',
                actions = [
                    PostbackAction(
                        label = '我要提升今明二日運勢',
                        display_text = '我要提升今明二日運勢',
                        data = 'action=service_1'
                    ),
                    PostbackAction(
                        label = '我想找出誰是我的貴人',
                        display_text = '我想找出誰是我的貴人',
                        data = 'action=service_2'
                    ),
                    PostbackAction(
                        label = '我想查詢老師諮詢時間',
                        display_text = '我想查詢老師諮詢時間',
                        data = 'action=service_3'
                    ),
                    PostbackAction(
                        label = '重新輸入生日及其它功能',
                        display_text = '重新輸入生日及其它功能',
                        data = 'action=service_4'
                    ),
                ]
            )
        )
    )
