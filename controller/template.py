# 任何需要客製化的文字以及圖片 template

from datetime import date, timedelta

from linebot.models import TemplateSendMessage, ButtonsTemplate, PostbackAction, URIAction, CarouselTemplate,\
    CarouselColumn


def main_menu_template(user_name):
    return TemplateSendMessage(
        alt_text = 'Buttons template',
        template = ButtonsTemplate(
            thumbnail_image_url = 'https://yt3.ggpht.com/-jHaW03KgtAc/AAAAAAAAAAI/AAAAAAAAAAA/9EFyOq-T5Ts/s900-c-k-no/photo.jpg',
            title = '運命所 OO 老師',
            text = '提升 [' + user_name + '] 運勢服務',
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


def service_2_menu_template():
    return TemplateSendMessage(
        alt_text = 'OO 老師 幫你找貴人',
        template = ButtonsTemplate(
            thumbnail_image_url = 'https://yt3.ggpht.com/-jHaW03KgtAc/AAAAAAAAAAI/AAAAAAAAAAA/9EFyOq-T5Ts/s900-c-k-no/photo.jpg',
            title = 'OO 老師 幫你找貴人',
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


def service_1_menu_template():
    return TemplateSendMessage(
        alt_text = 'OO 老師 協助您提升運勢',
        template = ButtonsTemplate(
            thumbnail_image_url = 'https://yt3.ggpht.com/-jHaW03KgtAc/AAAAAAAAAAI/AAAAAAAAAAA/9EFyOq-T5Ts/s900-c-k-no/photo.jpg',
            title = 'OO 老師 協助您提升運勢',
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


def service_3_menu_template():
    return TemplateSendMessage(
        alt_text = '預約 OO 老師',
        template = ButtonsTemplate(
            thumbnail_image_url = 'https://yt3.ggpht.com/-jHaW03KgtAc/AAAAAAAAAAI/AAAAAAAAAAA/9EFyOq-T5Ts/s900-c-k-no/photo.jpg',
            title = '預約 OO 老師',
            text = '您可以使用以下方式預約',
            actions = [
                PostbackAction(
                    label = '線上預約',
                    display_text = '現在 LINE 預約',
                    data = 'action=line_booking'
                ),
                URIAction(
                    label = '電話預約',
                    uri = 'tel://0912345678'
                ),
                PostbackAction(
                    label = '回主選單',
                    display_text = '回主選單',
                    data = 'action=show_menu'
                ),
            ]
        )
    )


def service_3_text():
    today = date.today()
    week_dict = {0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '日'}

    text = '最近一周 OO 老師可預約的時間如下：\n\n'\
           '1. '+(today+timedelta(days=0)).strftime('%m/%d')+' ( ' + week_dict[today.weekday()] + ' )' \
           ' 14:00、16:00、19:00\n' \
           '2. '+(today+timedelta(days=1)).strftime('%m/%d')+' ( ' + week_dict[(today+timedelta(days=1)).weekday()] + ' )' \
           ' 10:00、11:00\n' \
           '3. '+(today+timedelta(days=2)).strftime('%m/%d')+' ( ' + week_dict[(today+timedelta(days=2)).weekday()] + ' )' \
           ' 14:00、16:00、19:00\n' \
           '4. '+(today+timedelta(days=3)).strftime('%m/%d')+' ( ' + week_dict[(today+timedelta(days=3)).weekday()] + ' )' \
           ' 14:00、16:00、19:00\n' \
           '5. '+(today+timedelta(days=4)).strftime('%m/%d')+' ( ' + week_dict[(today+timedelta(days=4)).weekday()] + ' )' \
           ' 14:00、16:00、19:00\n' \
           '6. '+(today+timedelta(days=5)).strftime('%m/%d')+' ( ' + week_dict[(today+timedelta(days=5)).weekday()] + ' )' \
           ' 14:00、16:00、19:00\n' \
           '7. '+(today+timedelta(days=6)).strftime('%m/%d')+' ( ' + week_dict[(today+timedelta(days=6)).weekday()] + ' )' \
           ' 14:00、16:00、19:00\n' \

    return text


def line_booking_template():
    today = date.today()
    week_dict = {0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '日'}

    return TemplateSendMessage(
        alt_text = 'Carousel template',
        template = CarouselTemplate(
            columns = [
                CarouselColumn(
                    thumbnail_image_url = 'https://huangyedu.com/Data/Thumb/10/478de4b85b63532b18bc3b3cca0e48e1.jpg',
                    title = ' ',
                    text = today.strftime('%m/%d') + ' ( ' + week_dict[today.weekday()] + ' ) 預約時間',
                    actions = [
                        PostbackAction(
                            label = '14:00',
                            data = 'action=book_time&time=14:00&date=' + today.strftime('%m%d') + '&weekday=' +
                                   week_dict[today.weekday()]
                        ),
                        PostbackAction(
                            label = '16:00',
                            data = 'action=book_time&time=16:00&date=' + today.strftime('%m%d') + '&weekday=' +
                                   week_dict[today.weekday()]
                        ),
                        PostbackAction(
                            label = '19:00',
                            data = 'action=book_time&time=19:00&date=' + today.strftime('%m%d') + '&weekday=' +
                                   week_dict[today.weekday()]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://huangyedu.com/Data/Thumb/10/478de4b85b63532b18bc3b3cca0e48e1.jpg',
                    title = ' ',
                    text = (today + timedelta(days = 1)).strftime('%m/%d') + ' ( ' + week_dict[
                        (today + timedelta(days = 1)).weekday()] + ' ) 預約時間',
                    actions = [
                        PostbackAction(
                            label = '10:00',
                            data = 'action=book_time&time=10:00&date=' + (today + timedelta(days = 1)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 1)).weekday()]
                        ),
                        PostbackAction(
                            label = '11:00',
                            data = 'action=book_time&time=11:00&date=' + (today + timedelta(days = 1)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 1)).weekday()]
                        ),
                        PostbackAction(
                            label = '無',
                            data = 'action=book_time'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://huangyedu.com/Data/Thumb/10/478de4b85b63532b18bc3b3cca0e48e1.jpg',
                    title = ' ',
                    text = (today + timedelta(days = 2)).strftime('%m/%d') + ' ( ' + week_dict[
                        (today + timedelta(days = 2)).weekday()] + ' ) 預約時間',
                    actions = [
                        PostbackAction(
                            label = '14:00',
                            data = 'action=book_time&time=14:00&date=' + (today + timedelta(days = 2)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 2)).weekday()]
                        ),
                        PostbackAction(
                            label = '16:00',
                            data = 'action=book_time&time=16:00&date=' + (today + timedelta(days = 2)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 2)).weekday()]
                        ),
                        PostbackAction(
                            label = '19:00',
                            data = 'action=book_time&time=19:00&date=' + (today + timedelta(days = 2)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 2)).weekday()]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://huangyedu.com/Data/Thumb/10/478de4b85b63532b18bc3b3cca0e48e1.jpg',
                    title = ' ',
                    text = (today + timedelta(days = 3)).strftime('%m/%d') + ' ( ' + week_dict[
                        (today + timedelta(days = 3)).weekday()] + ' ) 預約時間',
                    actions = [
                        PostbackAction(
                            label = '14:00',
                            data = 'action=book_time&time=14:00&date=' + (today + timedelta(days = 3)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 3)).weekday()]
                        ),
                        PostbackAction(
                            label = '16:00',
                            data = 'action=book_time&time=16:00&date=' + (today + timedelta(days = 3)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 3)).weekday()]
                        ),
                        PostbackAction(
                            label = '19:00',
                            data = 'action=book_time&time=19:00&date=' + (today + timedelta(days = 3)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 3)).weekday()]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://huangyedu.com/Data/Thumb/10/478de4b85b63532b18bc3b3cca0e48e1.jpg',
                    title = ' ',
                    text = (today + timedelta(days = 4)).strftime('%m/%d') + ' ( ' + week_dict[
                        (today + timedelta(days = 4)).weekday()] + ' ) 預約時間',
                    actions = [
                        PostbackAction(
                            label = '14:00',
                            data = 'action=book_time&time=14:00&date=' + (today + timedelta(days = 4)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 4)).weekday()]
                        ),
                        PostbackAction(
                            label = '16:00',
                            data = 'action=book_time&time=16:00&date=' + (today + timedelta(days = 4)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 4)).weekday()]
                        ),
                        PostbackAction(
                            label = '19:00',
                            data = 'action=book_time&time=19:00&date=' + (today + timedelta(days = 4)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 4)).weekday()]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://huangyedu.com/Data/Thumb/10/478de4b85b63532b18bc3b3cca0e48e1.jpg',
                    title = ' ',
                    text = (today + timedelta(days = 5)).strftime('%m/%d') + ' ( ' + week_dict[
                        (today + timedelta(days = 5)).weekday()] + ' ) 預約時間',
                    actions = [
                        PostbackAction(
                            label = '14:00',
                            data = 'action=book_time&time=14:00&date=' + (today + timedelta(days = 5)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 5)).weekday()]
                        ),
                        PostbackAction(
                            label = '16:00',
                            data = 'action=book_time&time=16:00&date=' + (today + timedelta(days = 5)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 5)).weekday()]
                        ),
                        PostbackAction(
                            label = '19:00',
                            data = 'action=book_time&time=19:00&date=' + (today + timedelta(days = 5)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 5)).weekday()]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://huangyedu.com/Data/Thumb/10/478de4b85b63532b18bc3b3cca0e48e1.jpg',
                    title = ' ',
                    text = (today + timedelta(days = 6)).strftime('%m/%d') + ' ( ' + week_dict[
                        (today + timedelta(days = 6)).weekday()] + ' ) 預約時間',
                    actions = [
                        PostbackAction(
                            label = '14:00',
                            data = 'action=book_time&time=14:00&date=' + (today + timedelta(days = 6)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 6)).weekday()]
                        ),
                        PostbackAction(
                            label = '16:00',
                            data = 'action=book_time&time=16:00&date=' + (today + timedelta(days = 6)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 6)).weekday()]
                        ),
                        PostbackAction(
                            label = '19:00',
                            data = 'action=book_time&time=19:00&date=' + (today + timedelta(days = 6)).strftime(
                                '%m%d') + '&weekday=' + week_dict[(today + timedelta(days = 6)).weekday()]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://huangyedu.com/Data/Thumb/10/478de4b85b63532b18bc3b3cca0e48e1.jpg',
                    title = ' ',
                    text = '暫不預約',
                    actions = [
                        PostbackAction(
                            label = '暫不預約',
                            display_text = '暫不預約',
                            data = 'action=show_menu'
                        ),
                        PostbackAction(
                            label = '暫不預約',
                            display_text = '暫不預約',
                            data = 'action=show_menu'
                        ),
                        PostbackAction(
                            label = '暫不預約',
                            display_text = '暫不預約',
                            data = 'action=show_menu'
                        )
                    ]
                )
            ]
        )
    )


def fate_num_result_text(user_name):

    text = '[王小明] 對 [' + user_name + '] 的貴人指數分析如下：\n\n'\
             '財運貴人指數：★★★★☆\n'\
             '事業貴人指數：★★★☆☆\n'\
             '愛情貴人指數：★★☆☆☆\n\n'\
             '結論：\n'\
             '[王小明] 對 [' + user_name + '] 在財運上最有幫助。'
    return text


def love_fate_text(user_name):
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
    return text


def wealth_fate_text(user_name):
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
    return text


def service_2_instructions_text():
    text = '請對方加入以下的 OO 老師好運勢官方帳號: https://lin.ee/655qqady\n\n'\
           '再輸入姓名、生日以後，在主選單的「重新輸入生日以及其他功能」裡，按下查詢命盤編號，系統會顯示對方的命盤編號 '
    return text