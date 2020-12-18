#
# Custom Exceptions for the NotificationType Service
#

from sql_learning_app.api_vi.common import BaseApiException


class NotificationTypeDoesNotExist(BaseApiException):

    def __init__(self, id: int):
        msg = f'There is not NotificationType with id {id}'
        super().__init__(msg)
        self.status_code = 404


class EnableSourceDoesNotExist(BaseApiException):

    def __init__(self, name: str):
        msg = f'There is not Entity by the name {name}'
        super().__init__(msg)
        self.status_code = 404
