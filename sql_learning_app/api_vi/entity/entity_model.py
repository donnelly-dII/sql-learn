#
# To imlement Table Inheritance for our Users that can be people, Universities, or Organizations
# We need to create the base entity model class that can put all IDs in single spot with base information
# Like username, date started, and other shared data
#

# Local imports
from sql_learning_app.config import db


class EntityModel:

    def __init__(self, entity_name: str, entity_id: int = None, created_at: str = None):
        self.entity_name = entity_name

        # Optional args (might be assigned at creation)
        self.entity_id = entity_id
        self.created_at = created_at

    def to_rest(self):
        """DO NOT IMPLEMENT, Base class that is never accessed via API
        :return:
        """
        raise NotImplementedError('ILLEGAL OPERATION: Table "Entity" is a base model, cannot be serialized')

    def to_db(self) -> 'EntityDBModel':
        """Constructs a DB model
        :return: EntityDBModel object from this object
        """
        db_model = EntityDBModel()
        db_model.entity_name = self.entity_name
        db_model.created_at = self.created_at
        if self.entity_id:
            db_model.entity_id = self.entity_id
        return db_model

    @classmethod
    def from_db(cls, db_model: 'EntityDBModel') -> 'EntityModel':
        """Constructor from a DB object
        :return: EntityModel object from a DB row
        """
        return EntityModel(db_model.entity_name, db_model.entity_id, db_model.created_at)


class EntityDBModel(db.Model):
    __tablename__ = 'Entity'
    entity_id = db.Column(db.Integer, primary_key=True)
    entity_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
