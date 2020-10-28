from datetime import date

from linebot.models import TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction

from helper import utils


def service_1_menu_template(channel_id, user_name):
    return TemplateSendMessage(
        alt_text = utils.get_line_message(channel_id, 'service_1_menu_title').format(name=user_name),
        template = ButtonsTemplate(
            thumbnail_image_url = utils.get_line_message(channel_id, 'service_1_menu_image'),
            title = utils.get_line_message(channel_id, 'service_1_menu_title').format(name=user_name),
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


# TODO: 愛情運勢: 依照八字相關演算法計算
# TODO: 計算用戶過去三十天上線次數
def love_fate(channel_id, user_name):
    today = date.today()
    text = '[' + user_name + '] ' + str(today.month) + '月' + str(today.day) +\
           '日愛情運勢\n\n'\
           '今日愛情運勢：★★★★☆\n'\
           '今日愛情數字：6\n'\
           '今日愛情時間：09:00-10:00\n'\
           '今日愛情顏色：水晶紫\n\n'\
           '明日愛情運勢：★★★★★\n'\
           '明日愛情數字：9\n'\
           '明日愛情時間：19:00-20:00\n'\
           '明日愛情顏色：湖水藍\n\n'\
           '說明：顏色包含衣服、包包、鞋子、配件等皆可\n\n'\
           '[ △△ 運命所 OO 老師關心您，過去 30 天有 20 天見到過您 ]'

    template = [
        TextSendMessage(text = text),
        service_1_menu_template(channel_id, user_name)
    ]
    return template


# TODO: 財運運勢: 依照八字相關演算法計算
# TODO: 計算用戶過去三十天上線次數
def wealth_fate(channel_id, user_name):
    today = date.today()
    text = '[' + user_name + '] ' + str(today.month) + '月' + str(today.day) +\
           '日財運運勢\n\n'\
           '今日財運運勢：★★★★☆\n'\
           '今日財運數字：6\n'\
           '今日財運時間：09:00-10:00\n'\
           '今日財運顏色：水晶紫\n\n'\
           '明日財運運勢：★★★★★\n'\
           '明日財運數字：9\n'\
           '明日財運時間：19:00-20:00\n'\
           '明日財運顏色：湖水藍\n\n'\
           '說明：顏色包含衣服、包包、鞋子、配件等皆可\n\n'\
           '[ △△ 運命所 OO 老師關心您，過去 30 天有 20 天見到過您 ]'

    template = [
        TextSendMessage(text = text),
        service_1_menu_template(channel_id, user_name)
    ]
    return template
