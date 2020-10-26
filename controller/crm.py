from linebot.models import TemplateSendMessage, ConfirmTemplate, PostbackAction, TextSendMessage

from helper import utils


def confirm_name(event, line_bot_api, channel_id):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '請確認姓名',
            template = ConfirmTemplate(
                text = utils.get_line_message(channel_id, 'confirm_name').format(name=event.message.text),
                actions = [
                    PostbackAction(
                        label = '是',
                        display_text = '是',
                        data = 'action=confirm_name&reply=yes&name=' + event.message.text
                    ),
                    PostbackAction(
                        label = '否',
                        display_text = '否',
                        data = 'action=confirm_name&reply=no'
                    )
                ]
            )
        )
    )


def confirm_gender(event, line_bot_api, channel_id):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
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
    )


def input_birth_day(event, line_bot_api, channel_id, user_name):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = utils.get_line_message(channel_id, 'input_birth_day').format(name=user_name))
    )


def confirm_birth_day(event, line_bot_api, channel_id):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '請確認國曆生日',
            template = ConfirmTemplate(
                text = utils.get_line_message(channel_id, 'confirm_birth_day').format(year=event.message.text[:4],
                                                                                      month=event.message.text[4:6],
                                                                                      day=event.message.text[-2:]),
                actions = [
                    PostbackAction(
                        label = '是',
                        display_text = '是',
                        data = 'action=confirm_birth_day&reply=yes&birth_day=' + event.message.text
                    ),
                    PostbackAction(
                        label = '否',
                        display_text = '否',
                        data = 'action=confirm_birth_day&reply=no'
                    )
                ]
            )
        )
    )


def input_birth_time(event, line_bot_api, channel_id):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = utils.get_line_message(channel_id, 'input_birth_time'))
    )


def confirm_birth_time(event, line_bot_api, channel_id):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '請確認出生時間',
            template = ConfirmTemplate(
                text = utils.get_line_message(channel_id, 'confirm_birth_time').format(birth_time=event.message.text),
                actions = [
                    PostbackAction(
                        label = '是',
                        display_text = '是',
                        data = 'action=confirm_birth_time&reply=yes&birth_time=' + event.message.text
                    ),
                    PostbackAction(
                        label = '否',
                        display_text = '否',
                        data = 'action=confirm_birth_time&reply=no'
                    )
                ]
            )
        )
    )


def confirm_user_info(event, line_bot_api, channel_id, user_name, user_gender, user_birth_day, user_birth_time):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '確認所有資料',
            template = ConfirmTemplate(
                text = utils.get_line_message(channel_id, 'confirm_user_info').format(name=user_name,
                                                                                      gender=user_gender,
                                                                                      year=user_birth_day[:4],
                                                                                      month=user_birth_day[4:6],
                                                                                      day=user_birth_day[-2:],
                                                                                      birth_time=user_birth_time),
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
    )


def confirm_phone(event, line_bot_api, channel_id):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '請確認電話號碼',
            template = ConfirmTemplate(
                text = utils.get_line_message(channel_id, 'confirm_phone').format(phone=event.message.text),
                actions = [
                    PostbackAction(
                        label = '是',
                        display_text = '是',
                        data = 'action=confirm_phone&reply=yes&phone=' + event.message.text
                    ),
                    PostbackAction(
                        label = '否',
                        display_text = '否',
                        data = 'action=confirm_phone&reply=no'
                    )
                ]
            )
        )
    )