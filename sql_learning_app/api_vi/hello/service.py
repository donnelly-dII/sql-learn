from flask import current_app
from datetime import datetime

# Local Imports
from sql_learning_app.config import db
from .models import HelloModel


class HelloMessageService:

    def __init__(self):
        self.logger = current_app.logger

        self.db_session = db.session

    def create_new_hello_msg(self, hello: HelloModel) -> HelloModel:
        """INSERT a new Hello record to the DB
        :return: New Model
        """
        # fetch the new datetime
        time = datetime.now()
        hello.created_at = time
        self.db_session.add(hello.to_db())