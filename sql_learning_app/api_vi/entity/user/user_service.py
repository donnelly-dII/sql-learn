#
# DB Service for the User Table
#

from flask import current_app

# Local Imports
from sql_learning_app.config import db
from .user_model import UserModel, UserDBModel
from .user_exceptions import UserCreationException

# Imports from Parent Table/Object
from ..entity_model import EntityModel
from ..entity_service import EntityService
from ..entity_exceptions import EntityCreationException


class UserService:

    def __init__(self):
        self.logger = current_app.logger
        self.db_session = db.session

    def create_new_user(self, user: UserModel) -> UserModel:
        """Creates a new User object in the DB
        :param user: data model of the user
        :return: Created User with ID
        """
        # First Create a DB record in Entity Table
        print(user.__dict__)
        try:
            new_entity = EntityService().create_entity(EntityModel(user.user_type))
        except EntityCreationException as err:
            raise UserCreationException(f'Failed to create a new User object because an Entity could not be '
                                        f'created with exception {err}')
        # Now create a new User
        user_db_model = user.to_db()
        user_db_model.user_id = new_entity.entity_id
        self.db_session.add(user_db_model)
        self.db_session.commit()
        if not user_db_model:
            raise UserCreationException('Failed to create a new User')
        self.logger.info(f'Successfully Created a new User object with ID {user_db_model.user_id}')
        return UserModel.from_db(user_db_model)
