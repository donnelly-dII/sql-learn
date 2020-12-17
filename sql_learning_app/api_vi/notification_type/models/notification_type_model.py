#
# notification_type.models.notification_type_model: DB, local, and REST Schema for the NotificationType model
#

from marshmallow import Schema, fields, post_load, ValidationError

# Local imports
from sql_learning_app.config import db
from sql_learning_app.api_vi.common import InvalidRequest


class NotificationTypeRestModel(Schema):
    # Required Parameters
    entity_name = fields.String(required=True)
    entity_action = fields.String(required=True)

    # Optional parameters
    notification_type_id = fields.Integer()
    created_on = fields.DateTime()

    @post_load
    def make_notification_model(self, data: dict, **kwargs) -> 'NotificationTypeModel':
        """Deserializer for the Hello Object
        :param data: REST schema as a dictionary
        :return: NotificationTypeModel object
        """
        try:
            return NotificationTypeModel(**data)
        except ValidationError as err:
            raise InvalidRequest(err)


class NotificationTypeModel:

    def __init__(self, entity_name: str, entity_action: str,
                 notification_type_id: int = None, created_on: str = None):
        """Constructor for a NotificationTypeModel
        :param entity_name: Name of entity creating notification
        :param entity_action: Action taken on entity to create notification
        :param notification_type_id: primary key uid of notification_type
        :param created_on: date notification type added to DB
        """
        self.entity_name = entity_name
        self.entity_action = entity_action
        self.notification_type_id = notification_type_id
        self.created_on = created_on

    def to_rest(self) -> dict:
        """Convert data to REST model
        :return: dict of model data that can be sent via API return
        """
        return NotificationTypeRestModel().dump(self)

    def to_db(self) -> 'NotificationTypeDBModel':
        """Converts to DB model
        :return: NotificationTypeDBModel that matches this model
        """
        db_model = NotificationTypeDBModel()
        db_model.created_on = self.created_on
        db_model.entity_name = self.entity_name
        db_model.entity_action = self.entity_action
        if self.notification_type_id:
            db_model.notification_type_id = self.notification_type_id
        return db_model

    @classmethod
    def from_db(cls, db_model: 'NotificationTypeDBModel') -> 'NotificationTypeModel':
        """Constructor from a DB Model
        :param db_model:
        :return:
        """
        return NotificationTypeModel(db_model.entity_name, db_model.entity_action,
                                     db_model.notification_type_id, db_model.created_on)


class NotificationTypeDBModel(db.Model):
    __tablename__ = 'NotificationType'
    notification_type_id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False)
    entity_name = db.Column(db.String(50), nullable=False)
    entity_action = db.Column(db.String(50), nullable=False)
