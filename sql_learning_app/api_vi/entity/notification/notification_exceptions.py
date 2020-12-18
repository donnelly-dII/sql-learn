from sql_learning_app.api_vi.common import BaseApiException


class NotificationCreationException(Exception):
    pass


class InvalidSourceId(BaseApiException):
    def __init__(self, source_id: int):
        super().__init__(f'No Source entiity with id {source_id} could be found. '
                         f'Ensure that this source is an object of type "Entity"')
        self.status_code = 404
