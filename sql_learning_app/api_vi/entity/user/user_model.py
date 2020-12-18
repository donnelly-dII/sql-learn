#
# User Model is an entity in our application and therefore a child of the Entity Table
# User Model and Table is the parent table and object of the following user types:
#       Person
#       Organization
#

from marshmallow import Schema, fields, post_load, ValidationError

# Local imports
from sql_learning_app.config import db
from sql_learning_app.api_vi.common import InvalidRequest


class UserRestModel(Schema):
    user_id = fields.Integer(required=True)
    username = fields.String(required=True)
    user_type = fields.String(required=True)
    notifications_enabled = fields.Boolean()

    @post_load
    def make_notification_model(self, data: dict, **kwargs) -> 'UserModel':
        """Deserializer for the Hello Object
        :param data: REST schema as a dictionary
        :return: NotificationModel object
        """
        try:
            return UserModel(**data)
        except ValidationError as err:
            path = kwargs['path'] if 'path' in kwargs.keys() else None
            raise InvalidRequest(err, path)


class UserModel:

    def __init__(self, username: str, user_type: str, user_id: int = None, notifications_enabled: bool = False):
        self.username = username
        self.user_type = user_type
        self.user_id = user_id
        self.notifications_enabled = notifications_enabled

    def to_rest(self):
        """Base Table, no serailization
        :raises: NotImplementedError
        """
        return UserRestModel().dump(self)

    def to_db(self) -> 'UserDBModel':
        """Converts to the DB model representation
        :return: DB model of this data
        """
        db_model = UserDBModel()
        db_model.username = self.username
        db_model.user_type = self.user_type
        db_model.notifications_enabled = self.notifications_enabled
        if self.user_id:
            db_model.user_id = self.user_id

        return db_model

    @classmethod
    def from_db(cls, db_model: 'UserDBModel') -> 'UserModel':
        """Constructor from a UserDBModel
        :param db_model: DB model representation
        :return: UserModel from DB
        """
        return UserModel(db_model.username, db_model.user_type, db_model.user_id, db_model.notifications_enabled)


class UserDBModel(db.Model):
    __tablename__ = 'User'

    user_id = db.Column(db.Integer, db.ForeignKey('Entity.entity_id'), primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    user_type = db.Column(db.String(45), nullable=False, unique=True)
    notifications_enabled = db.Column(db.Boolean, default=False)

    # Add relationship with Entity
    db.relationship('Entity', backref='User', lazy=True)
