#
# API endpoint Resource for a User to fetch their Run Records
#

from flask_restful import Resource
from flask import current_app, request
from marshmallow import ValidationError

# Internal packages
from ..models import NotificationRestModel
from sql_learning_app.api_vi.entity.notification.services.notification_record_service import NotificationRecordService

# Internal Exceptions
from sql_learning_app.api_vi.common import BaseApiException, InvalidRequest


class UserNotificationResource(Resource):

    def __init__(self):
        self.logger = current_app.logger

        self.notification_serializer = NotificationRestModel()
        self.record_service = NotificationRecordService()

    def get(self, user_id: int):
        """GET operation for a user's run records
        :param user_id: UID of user
        :return: List of RunRecords
        """
        try:
            records = self.record_service.fetch_user_notifications(user_id)
            return [l.to_rest() for l in records]
        except BaseApiException as err:
            self.logger.error(f'Failed to Notification click redirect with error: {err}')
            return err.to_rest()
        except Exception as general_err:
            self.logger.critical(f'Failed to Notification click redireect with unhandled error {general_err}')
            return BaseApiException.from_exception(general_err).to_rest()
