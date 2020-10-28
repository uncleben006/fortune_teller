from linebot.models import TemplateSendMessage, ButtonsTemplate, PostbackAction

from helper import utils


def send_message(event, line_bot_api, message):
    line_bot_api.reply_message(
        event.reply_token,
        message
    )


def main_menu_template(channel_id, user_name):
    return TemplateSendMessage(
        alt_text = utils.get_line_message(channel_id, 'main_menu_title'),
        template = ButtonsTemplate(
            thumbnail_image_url = utils.get_line_message(channel_id, 'main_menu_image'),
            title = utils.get_line_message(channel_id, 'main_menu_title'),
            text = utils.get_line_message(channel_id, 'main_menu_text').format(name=user_name),
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