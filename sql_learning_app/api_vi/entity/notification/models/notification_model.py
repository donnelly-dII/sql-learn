#
# notification.models.notification_model: DB, local, and REST Schema for the Notification model
#
from marshmallow import Schema, fields, post_load, ValidationError

# Local imports
from sql_learning_app.config import db
from sql_learning_app.api_vi.common import InvalidRequest

# Imports from User
from sql_learning_app.api_vi.entity.user.user_model import UserDBModel, UserModel, UserRestModel


class NotificationRestModel(Schema):
    # Required Parameters
    notification_type_id = fields.Integer(required=True)
    source_id = fields.Integer(required=True)
    message = fields.String(required=True)
    recipients = fields.List(fields.Nested(UserRestModel), required=True)

    # Optional parameters
    notification_id = fields.Integer()

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
                 notification_id: int = None):
        """Constructor for a NotificationModel
        :param notification_type_id: ID of NotificationType
        :param source_id: entity_id of source entity
        :param message: notification message
        :param recipients: list of User recipients
        :param notification_id: Primary Key ID of Notification
        """
        # Required parameters
        self.notification_type_id = notification_type_id
        self.source_id = source_id
        self.message = message
        self.recipients = recipients

        # Optional to model (Could not be created yet
        self.notification_id = notification_id

    def to_rest(self) -> dict:
        """Creates REST formatted dictionary for return
        :return: NotificationRestModel of this data
        """
        return NotificationRestModel().dump(self)

    def to_db(self) -> 'NotificationDBModel':
        """Creates a DB model of this data
        :return: NotificationDBModel of the Notification
        """
        db_model = NotificationDBModel()
        db_model.message = self.message
        db_model.notification_type_id = self.notification_type_id
        db_model.source_id = self.source_id
        # Create DB models
        for recipient in self.recipients:
            db_model.recipients.append(recipient.to_db())

        # Optional Data of the ID
        if self.notification_id:
            db_model.notification_id = self.notification_id

        return db_model

    @classmethod
    def from_db(cls, db_model: 'NotificationDBModel') -> 'NotificationModel':
        """Constructor from a DB model
        :param db_model: NotificationDBModel to construct instance from
        :return: NotificationModel of the DB record
        """
        # Convert Recipients
        users = [UserModel.from_db(r) for r in db_model.recipients]
        return NotificationModel(db_model.notification_type_id, db_model.source_id, db_model.message,
                                 users, db_model.notification_id)


class NotificationDBModel(db.Model):
    __tablename__ = 'Notification'

    # Inherit Primary Key from entity
    notification_id = db.Column(db.Integer, db.ForeignKey('Entity.entity_id'), primary_key=True)
    db.relationship('Entity', backref='Notification', lazy=True)

    # Isolated Data
    message = db.Column(db.String(100), nullable=False)

    # Foreign Key Relationsips
    notification_type_id = db.Column(db.Integer, db.ForeignKey('NotificationType.notification_type_id'), nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey('Entity.entity_id'), nullable=False)

    # Many to Many Notifications -> Users
    notification_recipients = db.Table('NotificationHasUser',
                                       db.Column('user_id', db.Integer, db.ForeignKey('User.user_id'),
                                                 primary_key=True),
                                       db.Column('notification_id',
                                                 db.Integer,
                                                 db.ForeignKey('Notification.notification_id'),
                                                 primary_key=True))

    recipients = db.relationship('UserDBModel', secondary=notification_recipients, lazy='subquery',
                                 backref=db.backref('notifications', lazy=True))
