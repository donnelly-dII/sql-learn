#
#   hello.exceptions : Custom Exceptions for the Hello endpoint
#
from sql_learning_app.api_vi.common import BaseApiException


class HelloDoesntExist(BaseApiException):

    def __init__(self, id: int):
        msg = f'There is not Hello message with id {id}'
        super().__init__(msg)
        self.status_code = 404
