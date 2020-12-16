#
# hello.models.hello_model: DB, local, and REST Schema for the Hello World model
#
from marshmallow import Schema, fields, post_load, ValidationError

# Local imports
from sql_learning_app.config import db
from sql_learning_app.api_vi.common import InvalidRequest


class HelloRestModel(Schema):
    hello_id = fields.Integer()
    message = fields.String()
    created_at = fields.DateTime()

    @post_load
    def make_hello_model(self, data: dict, **kwargs) -> 'HelloModel':
        """Deserializer for the Hello Object
        :param data: REST schema as a dictionary
        :return: HelloModel object
        """
        try:
            return HelloModel(data['message'], hello_id=data['id'], created_at=data['created_at'])
        except ValidationError as err:
            raise InvalidRequest(err, '/hello')


class HelloModel:

    def __init__(self, message: str, hello_id: int = None, created_at: str = None):
        self.message = message
        self.hello_id = hello_id
        self.created_at = created_at

    def to_rest(self) -> dict:
        """Converts class object to REST format dictionary that can be returned
        :return: dictionary of data
        """
        return HelloRestModel().dump(self)

    def to_db(self) -> 'HelloDBModel':
        db_model = HelloDBModel()
        db_model.message = self.message
        db_model.created_at = self.created_at
        if self.hello_id:
            db_model.hello_id = self.hello_id
        return db_model

    @classmethod
    def from_db(cls, db_model: 'HelloDBModel') -> 'HelloModel':
        """Constructor for a HelloModel from the db one
        :param db_model: DB model representation to be converted
        :return: HelloModel from DB row
        """
        return HelloModel(db_model.message, db_model.hello_id, db_model.created_at)


class HelloDBModel(db.Model):
    hello_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), unique=True, nullable=False)
    created_at = db.Column(db.DateTime)
