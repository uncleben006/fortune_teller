from linebot.models import TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction

from helper import utils


def return_fate_num(channel_id):
    template = [
        TextSendMessage(text = '您的命盤編號為 168'),
        service_4_menu_template(channel_id)
    ]
    return template


def service_4_menu_template(channel_id):
    return TemplateSendMessage(
        alt_text = '重新輸入生日及其它功能',
        template = ButtonsTemplate(
            thumbnail_image_url = utils.get_line_message(channel_id, 'service_4_menu_image'),
            text = '重新輸入生日及其它功能',
            actions = [
                PostbackAction(
                    label = '重新輸入生日',
                    display_text = '重新輸入生日',
                    data = 'action=confirm_gender&status=confirm_gender'
                ),
                PostbackAction(
                    label = '查詢您的命盤編號',
                    display_text = '查詢命盤編號',
                    data = 'action=query_fate_num'
                ),
                PostbackAction(
                    label = '回主選單',
                    display_text = '回主選單',
                    data = 'action=show_menu'
                ),
            ]
        )
    )