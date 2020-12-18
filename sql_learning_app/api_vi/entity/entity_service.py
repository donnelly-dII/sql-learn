#
#   Database Service class for Entity Parent model
#


from flask import current_app
from datetime import datetime

# Local Imports
from sql_learning_app.config import db
from .entity_model import EntityModel, EntityDBModel

# Local exceptions
from .entity_exceptions import EntityCreationException


class EntityService:

    def __init__(self):
        self.logger = current_app.logger

        self.db_session = db.session

    def create_entity(self, entity: EntityModel) -> EntityModel:
        """INSERT a new Hello record to the DB
        :return: New Model
        :raises EntityCreationException if the Entity cannot be created
        """
        # Set current time
        time = datetime.now()
        entity.created_at = time
        # Write to DB
        db_model = entity.to_db()
        self.db_session.add(db_model)
        self.db_session.commit()
        if not db_model:
            raise EntityCreationException(f'Failed to create Entity of type {entity.entity_name}')
        self.logger.info(f'Created a new Entity record with ID {entity.entity_id}')
        return EntityModel.from_db(db_model)

    @staticmethod
    def verify_enable_name(entity_name: str) -> bool:
        """Ensures that an entity name is valid
        :param entity_name: name of entity
        :return: True if valid entity, False otherwise
        """
        first_name = EntityDBModel.query.filter_by(entity_name=entity_name).first()
        return first_name is not None
