class ApiMessage:
    detail = ''
    message_en = ''
    message_ru = ''

    def __str__(self):
        return self.detail

    def __repr__(self):
        return self.detail


class ApiMessages:
    class UserHasNoPermission(ApiMessage):
        detail = 'user_has_no_permission'
        message_en = 'User has no permission'
        message_ru = 'У пользователя нет прав'

    class UserDoesNotExist(ApiMessage):
        detail = 'user_does_not_exist'
        message_en = 'User does not exist'
        message_ru = 'Пользователь не существует'

