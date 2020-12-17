from flask import current_app
from datetime import datetime

# Local Imports
from .models import HelloModel, HelloDBModel
from sql_learning_app.config import db

# Local exceptions
from .exceptions import HelloDoesntExist
from sql_learning_app.api_vi.common import BaseApiException


class HelloMessageService:

    def __init__(self):
        self.logger = current_app.logger

        self.db_session = db.session

    def create_new_hello_msg(self, hello: HelloModel) -> HelloModel:
        """INSERT a new Hello record to the DB
        :return: New Model
        """
        # Set current time
        time = datetime.now()
        hello.created_at = time

        # Write to DB
        try:
            db_model = hello.to_db()
            # print(db_model).__dict__
            self.db_session.add(db_model)
            self.db_session.commit()
            return HelloModel.from_db(db_model)
        except Exception as err:
            print(err)

    def get_by_id(self, hello_id: int):
        """SELECT a Hello record by ID
        :return: HelloModel oject by ID
        :raises: HelloDoesntExist if the UID is not a valid primary key
        """
        try:
            hello = HelloDBModel.query.get(hello_id)
            if not hello:
                raise HelloDoesntExist(hello_id)
            return HelloModel.from_db(hello)
        except Exception as err:
            raise BaseApiException.from_exception(err)
