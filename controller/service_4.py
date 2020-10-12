from linebot.models import TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction


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


def service_4_menu_template():
    return TemplateSendMessage(
        alt_text = 'OO 老師 協助您提升運勢',
        template = ButtonsTemplate(
            thumbnail_image_url = 'https://yt3.ggpht.com/-jHaW03KgtAc/AAAAAAAAAAI/AAAAAAAAAAA/9EFyOq-T5Ts/s900-c-k-no/photo.jpg',
            title = 'OO 老師 協助您提升運勢',
            text = '請選擇想要提升哪種運勢？',
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