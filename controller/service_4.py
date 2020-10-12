from linebot.models import TextSendMessage

from controller.template import service_4_menu_template


def return_fate_num(event, line_bot_api):
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text = '您的命盤編號為 168'),
            service_4_menu_template()
        ]
    )


def service_4_menu(event, line_bot_api):
    line_bot_api.reply_message(
        event.reply_token,
        service_4_menu_template()
    )
