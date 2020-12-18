#
#   Service for interacting with NotificationType DB model
#
from datetime import datetime
from flask import current_app

# Local Imports
from sql_learning_app.config import db
from sql_learning_app.api_vi.admin.notification_type.notification_type_excpetions import NotificationTypeDoesNotExist
from sql_learning_app.api_vi.common import BaseApiException
from .models import NotificationTypeModel, NotificationTypeDBModel

# Local Exceptions
from .notification_type_excpetions import EnableSourceDoesNotExist, NotificationTypeCreationFailed

# Other Table Services
from sql_learning_app.api_vi.entity.entity_service import EntityService


class NotificationTypeService:
    def __init__(self):
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

        # Ensure that the Enity Type is real
        if not EntityService.verify_enable_name(notif_type.source_entity_name):
            raise EnableSourceDoesNotExist(notif_type.source_entity_name)

        # Write to DB
        db_model = notif_type.to_db()
        self.db_session.add(db_model)
        self.db_session.commit()
        if not db_model:
            raise
        try:
            db_model = notif_type.to_db()
            self.db_session.add(db_model)
            self.db_session.commit()
            return NotificationTypeModel.from_db(db_model)
        except Exception as err:
            print(err)

    def get_by_id(self, notification_type_id: int):
        """SELECT a NotificationType record by ID
        :param notification_type_id: UID of NotificationType
        :return: NotificationType oject by ID
        :raises: NotificationTypeDoesNotExist if the UID is not a valid primary key
        """
        try:
            notification_type = NotificationTypeDBModel.query.get(notification_type_id)
            if not notification_type:
                self.logger.error(f'Failed to fetch NotificationType by ID {notification_type_id} becasue it '
                                  f'does not exist')
                raise NotificationTypeDoesNotExist(notification_type_id)
            self.logger.info(f'NotificationType with id {notification_type_id} successfully fetched.')
            return NotificationTypeModel.from_db(notification_type)
        except Exception as err:
            raise BaseApiException.from_exception(err)
