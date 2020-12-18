#
# person.models.person_model : Data, Rest, DB object models for a Person
#

from marshmallow import Schema, fields, post_load, ValidationError

# Local imports
from sql_learning_app.config import db
from sql_learning_app.api_vi.common import InvalidRequest


class PersonRestModel(Schema):
    person_id = fields.Integer()
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)

    @post_load
    def make_person_model(self, data: dict, **kwargs) -> 'PersonModel':
        """Deserializer for the PersonModel Object
        :param data: REST schema as a dictionary
        :return: HelloModel object
        """
        try:
            return PersonModel(**data)
        except ValidationError as err:
            path = kwargs.get('path', None)
            raise InvalidRequest(err, path)


class PersonModel:

    def __init__(self, first_name: str, last_name: str = None, person_id: int = None):
        self.first_name = first_name
        self.last_name = last_name

        # Non-required args
        self.person_id = person_id

    def to_rest(self) -> dict:
        """Converts class object to REST format dictionary that can be returned
        :return: dictionary of data
        """
        return PersonRestModel().dump(self)

    def to_db(self) -> 'PersonDBModel':
        """Converts class object to a DB model
        :return: PersonDBModel representing this data
        """
        db_model = PersonDBModel()
        db_model.first_name = self.first_name
        db_model.last_name = self.last_name

        if self.person_id:
            db_model.person_id = self.person_id

        return db_model

    @classmethod
    def from_db(cls, db_model: 'PersonDBModel') -> 'PersonModel':
        """Constructor from a DB representation
        :param db_model: DB object of a Person
        :return: PersonModel object type of the person
        """
        return PersonModel(db_model.first_name, db_model.last_name, db_model.person_id)


class PersonDBModel(db.Model):
    __tablename__ = 'Person'

    person_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)

    # Add relationship with User
    db.relationship('User', backref='Person', lazy=True)
