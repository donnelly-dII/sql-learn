#
# notification.models.notification_model: DB, local, and REST Schema for the Notification model
#
from datetime import datetime
from marshmallow import Schema, fields, post_load, ValidationError

# Local imports
from sql_learning_app.config import db
from sql_learning_app.api_vi.common import InvalidRequest


class NotificationRestModel(Schema):
    # Required Parameters
    notification_type_id = fields.Integer(required=True)
    source_id = fields.Integer(required=True)
    message = fields.String(required=True)
    recipients = fields.List(fields.Integer, required=True)

    # Optional parameters
    notification_id = fields.Integer()
    created_on = fields.DateTime()

    @post_load
    def make_notification_model(self, data: dict, **kwargs) -> 'NotificationModel':
        """Deserializer for the Hello Object
        :param data: REST schema as a dictionary
        :return: NotificationModel object
        """
        try:
            return NotificationModel(**data)
        except ValidationError as err:
            path = kwargs['path'] if 'path' in kwargs.keys() else None
            raise InvalidRequest(err, path)


class NotificationModel:

    def __init__(self, notification_type_id: int, source_id: int, message: str, recipients: list,
                 notification_id: int = None, created_on: str = None):

        # Required parameters
        self.notification_type_id = notification_type_id
        self.source_id = source_id
        self.message = message
        self.recipients = recipients

        # Optional to model (Could not be created yet
        self.notification_id = notification_id
        self.created_on = created_on


class NotificationDBModel(db.Model):
    __tablename__ = 'Notification'
    notification_id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False)

    notification_type_id = db.relationship('NotificationType', backref='Notification', uselist=False, nullable=False)

    # Switch to Forgeign Key when created
    source_id = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)

    # recipients is a one to many relationship
    recipients = db.relationship('Entity', backref='notification', lazy=True)
