#
#  API controller for Notification Resource
#

from flask_restful import Resource
from flask import current_app, request
from marshmallow import ValidationError

# Internal packages
from ..models import NotificationRestModel
from sql_learning_app.api_vi.entity.notification.services.notification_service import NotificationService

# Internal Exceptions
from sql_learning_app.api_vi.common import BaseApiException, InvalidRequest


class NotificationResource(Resource):

    def __init__(self):
        self.logger = current_app.logger

        self.notification_serializer = NotificationRestModel()
        self.notification_service = NotificationService()

    def get(self):
        """GET operation to fetch all Hello World messages
        :return: List of all the records
        """
        pass

    def post(self):
        """POST to create a new Notification object
        :return: Notificaiton Object that is created
        """
        try:
            data = request.get_json()
            notification = self.notification_serializer.load(data)
        except ValidationError as err:
            return InvalidRequest(err).to_rest()

        # Create a new Hello Message with this model
        try:
            return self.notification_service.create_new_notification(notification).to_rest()
        except BaseApiException as internal_err:
            self.logger.error(f'Notification creation failed with the error: {internal_err}')
            return internal_err.to_rest()
        except Exception as general_err:
            self.logger.error(f'Notification creation failed with the error: {general_err}')
            return BaseApiException.from_exception(general_err).to_rest()
