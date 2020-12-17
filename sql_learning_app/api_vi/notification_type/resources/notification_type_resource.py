#
#  API controller for NotificationType resource
#

from flask_restful import Resource
from flask import current_app, request
from marshmallow import ValidationError

# Internal packages
from ..models import NotificationTypeRestModel
from ..service import NotificationTypeService

# Internal Exceptions
from sql_learning_app.api_vi.common import BaseApiException, InvalidRequest


URI = '/notificationtype'


class NotificationTypeResource(Resource):

    def __init__(self):
        self.logger = current_app.logger

        self.notification_type_serializer = NotificationTypeRestModel()
        self.notification_type_service = NotificationTypeService()

    def get(self):
        """GET operation to fetch all Hello World messages
        :return: List of all the records
        """
        pass

    def post(self):
        """POST to create a new Hello Message
        :return: NotificationType Object that is created
        """
        try:
            data = request.get_json()
            notification_type_model = self.notification_type_serializer.load(data)
        except ValidationError as err:
            return InvalidRequest(err).to_rest()

        # Create a new Notification Type
        try:
            return self.notification_type_service.create_new_notification_type(notification_type_model).to_rest()
        except BaseApiException as internal_err:
            self.logger.error(f'NotificationType creation failed with the error: {internal_err}')
            return internal_err.to_rest()
        except Exception as general_err:
            self.logger.error(f'NotificationType creation failed with the error: {general_err}')
            return BaseApiException.from_exception(general_err).to_rest()
