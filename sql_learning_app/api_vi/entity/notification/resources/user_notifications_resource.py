#
# API endpoint Resource for a User to fetch their Run Records
#

from flask_restful import Resource
from flask import current_app, request
from marshmallow import ValidationError

# Internal packages
from ..models import NotificationRestModel
from sql_learning_app.api_vi.entity.notification.services.notification_service import NotificationService

# Internal Exceptions
from sql_learning_app.api_vi.common import BaseApiException, InvalidRequest


class UserNotificationResource(Resource):

    def __init__(self):
        self.logger = current_app.logger

        self.notification_serializer = NotificationRestModel()
        self.notification_service = NotificationService()

    def get(self, user_id: int):
        """GET operation for a user's run records
        :param user_id: UID of user
        :return: List of RunRecords
        """
        pass