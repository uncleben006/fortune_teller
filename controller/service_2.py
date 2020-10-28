from linebot.models import TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction

from helper import utils


def service_2_menu_template(channel_id, user_name):
    return TemplateSendMessage(
        alt_text = utils.get_line_message(channel_id, 'service_2_menu_title').format(name=user_name),
        template = ButtonsTemplate(
            thumbnail_image_url = utils.get_line_message(channel_id, 'service_2_menu_image'),
            title = utils.get_line_message(channel_id, 'service_2_menu_title').format(name=user_name),
            text = '你知道對方的命盤編號嗎？',
            actions = [
                PostbackAction(
                    label = '我知道，我要輸入他的編號',
                    display_text = '我知道，我要輸入他的編號',
                    data = 'action=input_fate_num'
                ),
                PostbackAction(
                    label = '不知道，請告訴我怎麼做',
                    display_text = '不知道，請告訴我怎麼做',
                    data = 'action=ask_instructions'
                ),
                PostbackAction(
                    label = '回主選單',
                    display_text = '回主選單',
                    data = 'action=show_menu'
                ),
            ]
        )
    )


# TODO: 找貴人功能: 輸入了命盤編號後，要依照命盤編號找出對應的人的生辰時日，再計算彼此向性
def fate_num_result(channel_id, user_name):
    text = '[王小明] 對 [' + user_name + '] 的貴人指數分析如下：\n\n'\
            '財運貴人指數：★★★★☆\n'\
            '事業貴人指數：★★★☆☆\n'\
            '愛情貴人指數：★★☆☆☆\n\n'\
            '結論：\n'\
            '[王小明] 對 [' + user_name + '] 在財運上最有幫助。'

    template = [
        TextSendMessage(text = text),
        service_2_menu_template(channel_id, user_name)
    ]
    return template


def service_2_instructions(channel_id, user_name):
    text = utils.get_line_message(channel_id, 'service_2_instructions').format(name=user_name)
    template = [
        TextSendMessage(text = text),
        service_2_menu_template(channel_id, user_name)
    ]
    return template
