#
#
#

from flask import current_app
from multiprocessing.pool import ThreadPool
# Local Imports
from sql_learning_app.config import db
from sql_learning_app.api_vi.common import QueueService

from ..models import NotificationRecordModel, NotificationRecordDBModel

# Notification Imports
from ..models import NotificationModel

# User Imports
from sql_learning_app.api_vi.entity.user.user_model import UserModel

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