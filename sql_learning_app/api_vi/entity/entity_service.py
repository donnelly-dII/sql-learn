#
#   Database Service class for Entity Parent model
#


from flask import current_app
from datetime import datetime

# Local Imports
from sql_learning_app.config import db
from .entity_model import EntityModel, EntityDBModel

# Local exceptions
from .entity_exceptions import EntityCreationException, EntityDoesNotExist

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

    def fetch_entity_by_id(self, entity_id: int) -> EntityModel:
        """Fetches the Entity by ID
        :return: EntityModel from the DB row
        :raises: EntityDoesNotExist of no Entity of this type
        """
        # Fetch via primary key
        print(entity_id)
        db_model = EntityDBModel.query.get(entity_id)
        print('got here')
        print(db_model)
        if not db_model:
            self.logger.error(f'Could not fetch Entity with ID {entity_id} because it was not found')
            raise EntityDoesNotExist(entity_id)
        self.logger.info(f'Successfully Fetched Entity with id {entity_id}')
        return EntityModel.from_db(db_model)

    @staticmethod
    def verify_enable_name(entity_name: str) -> bool:
        """Ensures that an entity name is valid
        :param entity_name: name of entity
        :return: True if valid entity, False otherwise
        """
        first_name = EntityDBModel.query.filter_by(entity_name=entity_name).first()
        return first_name is not None
