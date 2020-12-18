from flask import current_app


# Local Imports
from .models import NotificationModel, NotificationDBModel
from .notification_exceptions import NotificationCreationException, InvalidSourceId

# Entity Imports
from ..entity_service import EntityService
from ..entity_model import EntityModel
from ..entity_exceptions import EntityCreationException, EntityDoesNotExist


class NotificationService:

    def __init__(self):
        self.logger = current_app.logger

    def create_new_notification(self, notification: NotificationModel) -> NotificationModel:
        """Creates a new Notification instance
        :param notification: Notification to push
        :return: Notification with Updated ID
        """
        entity_service = EntityService()
        # Ensure Source Enitty is valid
        try:
            entity_model = entity_service.fetch_entity_by_id(notification.source_id)
        except EntityDoesNotExist:
            raise InvalidSourceId(notification.source_id)

        # Create Root Entity
        try:
            new_entity = entity_service.create_entity(EntityModel(NotificationDBModel.__tablename__))
        except EntityCreationException as err:
            raise NotificationCreationException(f'Failed to create a new Notification because an Entity could not be '
                                                f'created with exception {err}')

        # Now Create a Notification
        notification_db_model = notification.to_db()
        person_db_model = person.to_db()
        person_db_model.person_id = new_user.user_id
        self.db_session.add(person_db_model)
        self.db_session.commit()
        if not person_db_model:
            raise PersonCreationException()
        self.logger.info(f'Successfully Created a new Person object with ID {person_db_model.person_id}')
        return PersonModel.from_db(person_db_model)