#
#   Service for interacting with NotificationType DB model
#
from datetime import datetime
from flask import current_app

# Local Imports
from sql_learning_app.config import db
from .models import NotificationTypeModel, NotificationTypeDBModel


class NotificationTypeService:

    def __int__(self):
        self.logger = current_app.logger

        self.db_session = db.session

    def create_new_notification_type(self, notif_type: NotificationTypeModel) -> NotificationTypeModel:
        """Create a new Notification Type entity in  the DB
        :param notif_type: NotificationType Data model to INSERT
        :return: NotificationType Data model with primary Key updated
        """
        # Set current time
        time = datetime.now()
        notif_type.created_on = time
        # Write to DB
        try:
            db_model = notif_type.to
            db_model = hello.to_db()
            # print(db_model).__dict__
            self.db_session.add(db_model)
            self.db_session.commit()
            return HelloModel.from_db(db_model)
        except Exception as err:
            print(err)

