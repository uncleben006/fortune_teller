from linebot.models import TemplateSendMessage, ConfirmTemplate, PostbackAction, TextSendMessage

from helper import utils


def confirm_name(channel_id, text):
    return TemplateSendMessage(
        alt_text = '請確認姓名',
        template = ConfirmTemplate(
            text = utils.get_line_message(channel_id, 'confirm_name').format(name = text),
            actions = [
                PostbackAction(
                    label = '是',
                    display_text = '是',
                    data = 'action=confirm_name&reply=yes&name=' + text
                ),
                PostbackAction(
                    label = '否',
                    display_text = '否',
                    data = 'action=confirm_name&reply=no'
                )
            ]
        )
    )


def confirm_gender(channel_id):
    return TemplateSendMessage(
        alt_text = '請確認性別',
        template = ConfirmTemplate(
            text = utils.get_line_message(channel_id, 'confirm_gender'),
            actions = [
                PostbackAction(
                    label = '男',
                    display_text = '男',
                    data = 'action=confirm_gender&reply=male'
                ),
                PostbackAction(
                    label = '女',
                    display_text = '女',
                    data = 'action=confirm_gender&reply=female'
                )
            ]
        )
    )


def input_birth_day(channel_id, user_name):
    return TextSendMessage(text = utils.get_line_message(channel_id, 'input_birth_day').format(name = user_name))


def confirm_birth_day(channel_id, text):
    template = TemplateSendMessage(
        alt_text = '請確認國曆生日',
        template = ConfirmTemplate(
            text = utils.get_line_message(channel_id, 'confirm_birth_day')\
                .format(year = text[:4], month = text[4:6], day = text[-2:]),
            actions = [
                PostbackAction(
                    label = '是',
                    display_text = '是',
                    data = 'action=confirm_birth_day&reply=yes&birth_day=' + text
                ),
                PostbackAction(
                    label = '否',
                    display_text = '否',
                    data = 'action=confirm_birth_day&reply=no'
                )
            ]
        )
    )
    return template


def input_birth_time(channel_id):
    return TextSendMessage(text = utils.get_line_message(channel_id, 'input_birth_time'))


def confirm_birth_time(channel_id, text):
    return TemplateSendMessage(
        alt_text = '請確認出生時間',
        template = ConfirmTemplate(
            text = utils.get_line_message(channel_id, 'confirm_birth_time').format(birth_time = text),
            actions = [
                PostbackAction(
                    label = '是',
                    display_text = '是',
                    data = 'action=confirm_birth_time&reply=yes&birth_time=' + text
                ),
                PostbackAction(
                    label = '否',
                    display_text = '否',
                    data = 'action=confirm_birth_time&reply=no'
                )
            ]
        )
    )


def confirm_user_info(channel_id, user_name, user_gender, user_birth_day, user_birth_time):
    text = utils.get_line_message(channel_id, 'confirm_user_info')\
        .format(name = user_name, gender = user_gender, year = user_birth_day[:4], month = user_birth_day[4:6],
                day = user_birth_day[-2:], birth_time = user_birth_time)

    template = TemplateSendMessage(
        alt_text = '確認所有資料',
        template = ConfirmTemplate(
            text = text,
            actions = [
                PostbackAction(
                    label = '是',
                    display_text = '是',
                    data = 'action=confirm_user_info&reply=yes'
                ),
                PostbackAction(
                    label = '否',
                    display_text = '否',
                    data = 'action=confirm_user_info&reply=no'
                )
            ]
        )
    )
    return template


def confirm_phone(channel_id, text):
    return TemplateSendMessage(
        alt_text = '請確認電話號碼',
        template = ConfirmTemplate(
            text = utils.get_line_message(channel_id, 'confirm_phone').format(phone = text),
            actions = [
                PostbackAction(
                    label = '是',
                    display_text = '是',
                    data = 'action=confirm_phone&reply=yes&phone=' + text
                ),
                PostbackAction(
                    label = '否',
                    display_text = '否',
                    data = 'action=confirm_phone&reply=no'
                )
            ]
        )
    )
