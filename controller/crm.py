from linebot.models import TemplateSendMessage, ConfirmTemplate, PostbackAction


def confirm_phone(event, line_bot_api):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '請確認電話號碼',
            template = ConfirmTemplate(
                text = '您的電話號碼是 ' + event.message.text + ' 嗎？',
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


def confirm_name(event, line_bot_api):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '請確認姓名',
            template = ConfirmTemplate(
                text = '您的姓名是 [' + event.message.text + '] 嗎？',
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


def confirm_birth_day(event, line_bot_api):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '請確認國曆生日',
            template = ConfirmTemplate(
                text = '您的國曆生日為 ' +
                       event.message.text[:4] + '年' + event.message.text[4:6] + '月' + event.message.text[-2:] + '日 嗎？',
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


def confirm_birth_time(event, line_bot_api):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '請確認出生時間',
            template = ConfirmTemplate(
                text = '您的出生時間為 ' + event.message.text + ' 嗎？',
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


def confirm_gender(event, line_bot_api):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '請確認性別',
            template = ConfirmTemplate(
                text = '您的性別為',
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


def confirm_user_info(event, line_bot_api, user_name, user_gender, user_birth_day, user_birth_time):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text = '確認所有資料',
            template = ConfirmTemplate(
                text = '您是 [' + user_name + '], ' + user_gender + '性, 生日為 ' +
                       user_birth_day[:4] + '/' + user_birth_day[4:6] + '/' + user_birth_day[-2:] +
                       ' ' + user_birth_time + ' ?',
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