from linebot.models import TextSendMessage


from controller.template import service_1_menu_template, love_fate_text, wealth_fate_text


# TODO: 1. 要依照八字相關演算法計算
def love_fate_result(event, line_bot_api, user_name):
    text = love_fate_text(user_name)
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text = text),
            service_1_menu_template()
        ]
    )


# TODO: 依照八字相關演算法計算
def wealth_fate_result(event, line_bot_api, user_name):
    text = wealth_fate_text(user_name)
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


