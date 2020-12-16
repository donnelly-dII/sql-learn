from flask import current_app
from datetime import datetime

# Local Imports
from .models import HelloModel
from sql_learning_app.config import db


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
