#
# hello.models.hello_model: DB, local, and REST Schema for the Hello World model
#
from marshmallow import Schema, fields, post_load, ValidationError


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
        self.id = hello_id
        self.created_at = created_at

    def to_rest(self) -> dict:
        """Converts class object to REST format dictionary that can be reterned
        :return: dictionary of data
        """
        return HelloRestModel().dump(self)


class HelloDBSchema:
    pass