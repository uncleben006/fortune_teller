from datetime import date, timedelta

from linebot.models import TextSendMessage, TemplateSendMessage, PostbackAction, ConfirmTemplate, ButtonsTemplate,\
    URIAction, CarouselTemplate, CarouselColumn
from messages.general import main_menu_template
from helper import utils


# TODO: 新增 channel info table，讓命理師紀錄自己每週可以預約的時間
def service_3_menu(channel_id, user_name):
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

    template = TemplateSendMessage(
        alt_text = utils.get_line_message(channel_id, 'service_3_menu_title').format(name=user_name),
        template = ButtonsTemplate(
            thumbnail_image_url = utils.get_line_message(channel_id, 'service_3_menu_image').format(name=user_name),
            title = utils.get_line_message(channel_id, 'service_3_menu_title').format(name=user_name),
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

    template = [
        TextSendMessage(text = text),
        template
    ]
    return template


def confirm_book_time(book_date, weekday, time):
    return TemplateSendMessage(
        alt_text = '確認預約時間',
        template = ConfirmTemplate(
            text = '您要預約 ' + book_date[:2] + '月' + book_date[-2:] +
                   '日 (' + weekday + ') ' + time + ' 嗎？',
            actions = [
                PostbackAction(
                    label = '是',
                    display_text = '是',
                    data = 'action=confirm_book_time&reply=yes'
                ),
                PostbackAction(
                    label = '否',
                    display_text = '否',
                    data = 'action=confirm_book_time&reply=no'
                )
            ]
        )
    )


def input_phone(channel_id, user_name):
    return TextSendMessage(
        text = utils.get_line_message(channel_id, 'input_phone').format(name = user_name)
    )


def line_booking_template():
    today = date.today()
    week_dict = {0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '日'}
    week_img = {
        0: 'https://d2q275vdzul5bt.cloudfront.net/vassets/cfac4ec522dc6c13297b2df81d288b3b96d96e97/socialThumb.jpg',
        1: 'https://image.shutterstock.com/image-vector/word-tuesday-colorful-day-week-260nw-1285201639.jpg',
        2: 'https://www.thefactsite.com/wp-content/uploads/2017/07/wednesday-facts.jpg',
        3: 'https://img3.stockfresh.com/files/e/enterlinedesign/m/88/7684297_stock-photo-thursday-colorful-watercolor-and-ink-word-art.jpg',
        4: 'https://www.brookesandco.net/wp-content/uploads/2018/03/Brookes-Co-Friday-Feeling.jpg',
        5: 'https://i.pinimg.com/originals/9e/bf/24/9ebf24a0b925137494ec586f1dbfce2d.jpg',
        6: 'https://static.vecteezy.com/system/resources/previews/000/135/921/original/vector-sunday-lettering-watercolor.jpg'
    }

    return TemplateSendMessage(
        alt_text = '預約時間',
        template = CarouselTemplate(
            columns = [
                CarouselColumn(
                    thumbnail_image_url = week_img[today.weekday()],
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
                    thumbnail_image_url = week_img[(today + timedelta(days = 1)).weekday()],
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
                    thumbnail_image_url = week_img[(today + timedelta(days = 2)).weekday()],
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
                    thumbnail_image_url = week_img[(today + timedelta(days = 3)).weekday()],
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
                    thumbnail_image_url = week_img[(today + timedelta(days = 4)).weekday()],
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
                    thumbnail_image_url = week_img[(today + timedelta(days = 5)).weekday()],
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
                    thumbnail_image_url = week_img[(today + timedelta(days = 6)).weekday()],
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
                    thumbnail_image_url = 'https://cdn1.vectorstock.com/i/1000x1000/58/45/mission-aborted-rubber-stamp-vector-12765845.jpg',
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


def booking_result(channel_id, user_name, phone, book_date, weekday, time):

    text = utils.get_line_message(channel_id, 'booking_result')\
        .format(name=user_name,
                book_time=book_date[:2] + '月' + book_date[-2:] + '日 ( ' + weekday + ' ) ' + time,
                phone=phone)

    template = [
        TextSendMessage(text = text),
        main_menu_template(channel_id, user_name)
    ]

    return template
