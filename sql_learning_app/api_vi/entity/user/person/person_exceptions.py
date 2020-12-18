from sql_learning_app.api_vi.common import BaseApiException


class PersonNotFound(BaseApiException):

    def __init__(self, id: int):
        msg = f'No such person with ID {id} exists'
        super().__init__(msg)
        self.status_code = 404


class PersonCreationException(BaseApiException):

    def __init__(self, err: Exception = None):
        msg = 'Failed to create new Person record'
        if err:
            msg += f' with exception {err}'
        super().__init__(msg)
        self.status_code = 500
