from flask import current_app


# Local Imports
from sql_learning_app.config import db
from .models import NotificationModel, NotificationDBModel
from .notification_exceptions import NotificationCreationException, InvalidSourceId, InvalidNotificationType

# NotificationType Imports
from sql_learning_app.api_vi.admin.notification_type.notification_type_service import NotificationTypeService
from sql_learning_app.api_vi.admin.notification_type.notification_type_excpetions import NotificationTypeDoesNotExist


# Entity Imports
from ..entity_service import EntityService
from ..entity_model import EntityModel
from ..entity_exceptions import EntityCreationException, EntityDoesNotExist


class NotificationService:

    def __init__(self):
        self.logger = current_app.logger
        self.db_session = db.session

    def create_new_notification(self, notification: NotificationModel) -> NotificationModel:
        """Creates a new Notification instance
        :param notification: Notification to push
        :return: Notification with Updated ID
        """
        # Validate the input data
        self.__validate_notification_data(notification)

        # Create Root Entity
        try:
            new_entity = EntityService().create_entity(EntityModel(NotificationDBModel.__tablename__))
        except EntityCreationException as err:
            raise NotificationCreationException(f'Failed to create a new Notification because an Entity could not be '
                                                f'created with exception {err}')

        # Now Create a Notification
        notification_db_model = notification.to_db()
        notification_db_model.notification_id = new_entity.entity_id
        self.db_session.add(notification_db_model)
        self.db_session.commit()
        if not notification_db_model:
            self.logger.error(f'Failed to Create Notification due to DB error')
            raise NotificationCreationException()
        self.logger.info(f'Successfully created new notification with ID {notification_db_model.notification_id}')
        return NotificationModel.from_db(notification_db_model)

    def __validate_notification_data(self, notification: NotificationModel):
        """Checks a Notification's data and validates that it is valid and real
        :param notification: NotificationModel to be checked
        :return: Void
        :raises: InvalidSourceId if Notification has invalid source_id
        :raises: InvalidNotificationType if Notification has invalid notification_type_id
        """
        try:
            print(notification.source_id)
            EntityService().fetch_entity_by_id(notification.source_id)
            NotificationTypeService().get_by_id(notification.notification_type_id)

        except EntityDoesNotExist as ent_err:
            self.logger.error(f'Notification with message {notification.message} has invalid '
                              f'source_id withe error {ent_err}')
            raise InvalidSourceId(notification.source_id)

        except NotificationTypeDoesNotExist as notif_type_err:
            self.logger.error(f'Notification with message {notification.message} has invalid '
                              f'notification_type_id withe error {notif_type_err}')
            raise InvalidNotificationType(notification.notification_type_id)
