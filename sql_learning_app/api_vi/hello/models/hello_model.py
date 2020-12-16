#
# hello.models.hello_model: DB, local, and REST Schema for the Hello World model
#
from marshmallow import Schema, fields, post_load, ValidationError

# Local imports
from sql_learning_app.config import db


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
            print('handle this at higher level')


class HelloModel:

    def __init__(self, message: str, hello_id: int = None, created_at: str = None):
        self.message = message
        self.hello_id = hello_id
        self.created_at = created_at

    def to_rest(self) -> dict:
        """Converts class object to REST format dictionary that can be reterned
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


class HelloDBModel(db.Model):
    hello_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), unique=True, nullable=False)
    created_at = db.Column(db.DateTime)
