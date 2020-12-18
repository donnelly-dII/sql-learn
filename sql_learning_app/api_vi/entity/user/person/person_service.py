#
# Person Service class to interact with the Person DB Table
#

from flask import current_app
from datetime import datetime

# Local Imports
from .models import PersonModel, PersonDBModel
from sql_learning_app.config import db

# Parent Imports
from ..user_model import UserModel
from ..user_service import UserService
from ..user_exceptions import UserCreationException

# Local exceptions
from .person_exceptions import PersonCreationException


class PersonService:

    def __init__(self):
        self.logger = current_app.logger
        self.db_session = db.session

    def create_new_person(self, person: PersonModel) -> PersonModel:
        """Creates a new person object in the DB
        :param person:
        :return:
        """
        # First Create a User row
        try:
            new_user = UserService().create_new_user(UserModel(PersonDBModel.__tablename__))
        except UserCreationException as err:
            raise PersonCreationException(err)
        # Now Create a Person
        person_db_model = person.to_db()
        person_db_model.person_id = new_user.user_id
        self.db_session.add(person_db_model)
        self.db_session.commit()
        if not person_db_model:
            raise PersonCreationException()
        self.logger.info(f'Successfully Created a new Person object with ID {person_db_model.person_id}')
        return PersonModel.from_db(person_db_model)
