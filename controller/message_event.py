from linebot.models import TextSendMessage


def handle(event, line_bot_api):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = event.message.text))