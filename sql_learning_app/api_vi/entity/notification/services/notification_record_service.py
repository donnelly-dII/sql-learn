#
#
#

from flask import current_app
# Local Imports
from sql_learning_app.config import db
from sql_learning_app.api_vi.common import QueueService

from ..models import NotificationRecordModel, NotificationRecordDBModel

from sql_learning_app.api_vi.entity.user.user_model import UserDBModel

# Notification Imports
from ..models import NotificationModel, NotificationDBModel, UserNotificationRecord
from sql_learning_app.api_vi.admin.notification_type.models import NotificationTypeDBModel, NotificationTypeModel

# Exception imports
from ..notification_exceptions import NotificationRecordDoesNotExist
from sql_learning_app.api_vi.admin.notification_type.notification_type_excpetions import NotificationTypeDoesNotExist

# Can make configurable Env variable
POOL_MAX = 10


class NotificationRecordService:

    def __init__(self):
        self.logger = current_app.logger
        self.db_session = db.session

        # Import the abstract Queue for demo purposes
        self.record_queue = QueueService('Notifications')

    def run_records(self, notification: NotificationModel):
        """Runs a notification by making a NotificationRecord for each recipient, and sending it via the Queue
        :param notification: New Notification to be sent to users
        :return: Void, passive send
        """
        if notification.recipients and len(notification.recipients) > 0:
            for r in notification.recipients:
                self.__run_record_thread((notification, r))

            #record_packages = [(notification, recipient) for recipient in notification.recipients]
            #pool_size = min(len(notification.recipients), POOL_MAX)
            #pool = ThreadPool(pool_size)
            #pool.map(self.__run_record_thread, record_packages)

    def __run_record_thread(self, record_package: tuple):
        """Creates single RunRecord for
        ":param: record_package is a tuple of the notification and recipient
        :return:
        """
        notification = record_package[0]
        recipient = record_package[1]
        # Create the DB instance before sending
        record_model = NotificationRecordModel(notification.notification_id, recipient.user_id)
        record_db_model = record_model.to_db()
        self.db_session.add(record_db_model)
        self.db_session.commit()
        if not record_db_model:
            self.logger.error(f'Failed to create NotificationRunRecord for User with ID {recipient.user_id}')

        # With a new Record, add a message to the Notification Queue
        self.record_queue.enqueue(notification.message, recipient.user_id)

    def fetch_redirect_url(self, notification_record_id: int):
        """Constructs the 'onClick' redirect url of a notification record
        :param notification_record_id: DB ID of notification_record
        :return: redirect url to source entity
        """
        notification_query = "select notification_type_id, source_id from learn_sql_schema.Notification " \
                             "where notification_id=" \
                             "(Select notification_id from learn_sql_schema.NotificationRecord " \
                             f"where notification_record_id = {notification_record_id})"

        result = list(self.db_session.execute(notification_query))
        if len(result) == 0:
            raise NotificationRecordDoesNotExist(record_id=notification_record_id)
        type_id = result[0][0]
        source_id = result[0][1]

        # Now fetch the redirect URL
        type_model = NotificationTypeDBModel.query.get(type_id)
        if not type_model:
            raise NotificationTypeDoesNotExist(type_id)
        notif_type = NotificationTypeModel.from_db(type_model)
        return f'{notif_type.entity_redirect_uri}/{source_id}'

    def fetch_user_notifications(self, user_id: int) -> list:
        """
        :return:
        """
        records = NotificationRecordDBModel.query.filter_by(recipient_id=user_id).all()
        if not records:
            raise Exception(f"no recoreds found for user {user_id}")

        # Fetch the user
        user = UserDBModel.query.get(user_id)
        username = user.username

        # Now for each NotificationRecord we need to Fetch the Notification to know the message
        user_notifications = []
        for record in records:
            # Fetch the Notification
            _notif = UserNotificationRecord(user_id, record.notification_record_id, username=username)
            notification = NotificationDBModel.query.get(record.notification_id)
            _notif.message = notification.message
            user_notifications.append(_notif)

        self.logger.info(f'Fetched all records for User {user_id}')
        return user_notifications

