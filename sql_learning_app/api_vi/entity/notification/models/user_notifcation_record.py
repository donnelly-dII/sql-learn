#
# Helper Rest class for UserNotifications
#

from marshmallow import Schema, fields, post_load, ValidationError

# Local imports
from sql_learning_app.config import db
from sql_learning_app.api_vi.common import InvalidRequest


class UserNotificationRecordRestModel(Schema):
    recipient_id = fields.String()
    record_id = fields.String()

    username = fields.String()
    message = fields.String()

    # Optional parameters
    notification_record_id = fields.Integer()

    @post_load
    def make_notification_model(self, data: dict, **kwargs) -> 'UserNotificationRecord':
        """Deserializer for the Hello Object
        :param data: REST schema as a dictionary
        :return: NotificationModel object
        """
        try:
            return UserNotificationRecord(**data)
        except ValidationError as err:
            path = kwargs['path'] if 'path' in kwargs.keys() else None
            raise InvalidRequest(err, path)


class UserNotificationRecord:

    def __init__(self, recipient_id: int, record_id: int, username: str = None, message: str = None):
        """Class for holding Usernotification info
        :param recipient_id: ID of recipient user
        :param record_id: ID of NotificationRecord
        :param username: username of user
        :param message: Message in notification
        """
        self.recipient_id = recipient_id
        self.record_id = record_id
        self.username = username
        self.message = message

    def to_rest(self) -> dict:
        """Creates REST formatted dictionary for return
        :return: NotificationRestModel of this data
        """
        return UserNotificationRecordRestModel().dump(self)
