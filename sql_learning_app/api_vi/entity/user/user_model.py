#
# User Model is an entity in our application and therefore a child of the Entity Table
# User Model and Table is the parent table and object of the following user types:
#       Person
#       Organization
#

# Local imports
from sql_learning_app.config import db


class UserModel:

    def __init__(self, user_name: str, user_id: int = None, notifications_enabled: bool = False):
        self.user_name = user_name
        self.user_id = user_id
        self.notifications_enabled = notifications_enabled

    def to_rest(self):
        """Base Table, no serailization
        :raises: NotImplementedError
        """
        raise NotImplementedError('ILLEGAL OPERATION : Model "User" cannot be serialized '
                                  'because it is not accessible by API')

    def to_db(self) -> 'UserDBModel':
        """Converts to the DB model representation
        :return: DB model of this data
        """
        db_model = UserDBModel()
        db_model.user_name = self.user_name
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
        return UserModel(db_model.user_name, db_model.user_id, db_model.notifications_enabled)


class UserDBModel(db.Model):
    __tablename__ = 'User'

    user_id = db.Column(db.Integer, db.ForeignKey('Entity.entity_id'), primary_key=True)
    user_name = db.Column(db.String(45), nullable=False)
    notifications_enabled = db.Column(db.Boolean, default=False)

    # Add relationship with Entity
    db.relationship('Entity', backref='User', lazy=True)
