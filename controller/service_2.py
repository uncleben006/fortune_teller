from linebot.models import TextSendMessage
from controller.template import service_2_menu_template, service_2_instructions_text, fate_num_result_text


def ask_instructions(event, line_bot_api):
    text = service_2_instructions_text()
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text = text),
            service_2_menu_template()
        ]
    )


def service_2_menu(event, line_bot_api):
    line_bot_api.reply_message(
        event.reply_token,
        service_2_menu_template()
    )


def fate_num_result(event, line_bot_api, user_name):
    text = fate_num_result_text(user_name)
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text = text),
            service_2_menu_template()
        ]
    )