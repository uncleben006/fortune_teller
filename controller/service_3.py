from linebot.models import TextSendMessage, TemplateSendMessage, PostbackAction, ConfirmTemplate

from controller.template import main_menu_template, service_3_menu_template, service_3_text, line_booking_template


def service_3_menu(event, line_bot_api):
    text = service_3_text()
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text = text),
            service_3_menu_template()
        ]
    )


def line_booking(event, line_bot_api):
    line_bot_api.reply_message(
        event.reply_token,
        line_booking_template()
    )


def confirm_book_time(event, line_bot_api, book_date, weekday, time):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '確認預約時間',
            template = ConfirmTemplate(
                text = '您要預約 ' + book_date[:2] + '月' + book_date[-2:] +
                       '日 (' + weekday + ') ' + time + ' 嗎？',
                actions = [
                    PostbackAction(
                        label = '是',
                        display_text = '是',
                        data = 'action=confirm_book_time&reply=yes'
                    ),
                    PostbackAction(
                        label = '否',
                        display_text = '否',
                        data = 'action=confirm_book_time&reply=no'
                    )
                ]
            )
        )
    )


def booking_result(event, line_bot_api, user_name, phone, book_date, weekday, time):
    text = '[' + user_name + '] 您好，以下是您預約資料：\n\n'\
                             '1. 時間：' + book_date[:2] + '月' + book_date[-2:] + '日 ( ' + weekday + ' ) ' + time + '\n'\
                             '2. 地址：OO市OO區OO路OO號\n'\
                             '3. 電話：' + phone + '\n\n'\
                             '若有要調整預約時間或其它問題，可以在此客服機器人上留言，或打 0912345678 聯絡 OO 老師'
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text = text),
            main_menu_template(user_name)
        ]
    )
