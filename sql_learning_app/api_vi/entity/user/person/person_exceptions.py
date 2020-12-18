from sql_learning_app.api_vi.common import BaseApiException


class PersonCreationException(BaseApiException):

    def __init__(self, err: Exception = None):
        msg = 'Failed to create new Person record'
        if err:
            msg += f' with exception {err}'
        super().__init__(msg)
        self.status_code = 500
