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
            path = kwargs['path'] if 'path' in kwargs.keys() else None
            raise InvalidRequest(err, path)


class NotificationTypeModel:

    def __int__(self, entity_name: str, entity_action: str,
                notification_type_id: int = None, created_on: str = None):
        """Constructor for a NotificationType
        :param entity_name: Name of DB entity that triggers a Notification of this type
        :param entity_action: The action taken on this entity that creates a notification
        :param notification_type_id: Primary Key ID of entity type
        :param created_on: Date entity type was created
        """
        self.entity_name = entity_name
        self.entity_action = entity_action

        # Optional parameters
        self.notification_type_id = fields.Integer()
        self.created_on = fields.DateTime()


class NotificationTypeDBModel(db.Model):

    notification_type_id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False)
    entity_name = db.Column(db.String(50), nullable=False)
    entity_action = db.Column(db.String(50), nullable=False)
