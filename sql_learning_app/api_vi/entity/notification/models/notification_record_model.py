#
# notification.models.notification_record_model: DB, local, and REST Schema for the NotificationRecord model
#
from marshmallow import Schema, fields, post_load, ValidationError

# Local imports
from sql_learning_app.config import db
from sql_learning_app.api_vi.common import InvalidRequest


class NotificationRecordRestModel(Schema):
    # Required Parameters
    notification_id = fields.Integer(required=True)
    recipient_id = fields.Integer(required=True)
    delivered = fields.Boolean()
    read = fields.Boolean()

    # Optional parameters
    notification_record_id = fields.Integer()

    @post_load
    def make_notification_model(self, data: dict, **kwargs) -> 'NotificationRecordModel':
        """Deserializer for the Hello Object
        :param data: REST schema as a dictionary
        :return: NotificationModel object
        """
        try:
            return NotificationRecordModel(**data)
        except ValidationError as err:
            path = kwargs['path'] if 'path' in kwargs.keys() else None
            raise InvalidRequest(err, path)


class NotificationRecordModel:
    def __init__(self, notification_id: int, recipient_id: int, delivered: bool = False,
                 read: bool = False, notification_record_id: int = None):
        """Constructor for a NotificationRecordModel
        :param notification_id: ID of the notification generating the record
        :param recipient_id: ID of the recipient recieving the record
        :param delivered: True if notification delivered, False otherwise
        :param read: True if notification read, False otherwise
        :param notification_record_id: UID of the notification record
        """
        self.notification_id = notification_id
        self.recipient_id = recipient_id
        self.delivered = delivered
        self.read = read
        self.notification_record_id = notification_record_id

    def to_rest(self) -> dict:
        """Creates REST formatted dictionary for return
        :return: NotificationRestModel of this data
        """
        return NotificationRecordRestModel().dump(self)

    def to_db(self) -> 'NotificationRecordDBModel':
        """Creates a DB model of this data
        :return: NotificationRecordDBModel of the Notification
        """
        db_model = NotificationRecordDBModel()
        db_model.notification_id = self.notification_id
        db_model.recipient_id = self.recipient_id
        db_model.read = self.read
        db_model.delivered = self.delivered

        if self.notification_record_id:
            db_model.notification_record_id = self.notification_record_id

        return db_model

    @classmethod
    def from_db(cls, db_model: 'NotificationRecordDBModel') -> 'NotificationRecordModel':
        """Constructor from a DB model
        :param db_model: NotificationRecordDBModel to construct instance from
        :return: NotificationRecordModel of the DB record
        """
        return NotificationRecordModel(db_model.notification_id, db_model.recipient_id, db_model.delivered,
                                       db_model.read, db_model.notification_record_id)


class NotificationRecordDBModel(db.Model):
    __tablename__ = 'NotificationRecord'
    notification_record_id = db.Column(db.Integer, primary_key=True)

    notification_id = db.Column(db.Integer, db.ForeignKey('Notification.notification_id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)

    delivered = db.Column(db.Boolean, nullable=False, default=False)
    read = db.Column(db.Boolean, nullable=False, default=False)
