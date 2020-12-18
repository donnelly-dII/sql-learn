#
#  API controller for NotificationType resource
#

from flask_restful import Resource
from flask import current_app

# Internal packages
from sql_learning_app.api_vi.admin.notification_type.notification_type_service import NotificationTypeService

# Internal Exceptions
from sql_learning_app.api_vi.common import BaseApiException

URI = '/notificationtype/<int:notification_type_id>'


class NotificationTypeIdResource(Resource):

    def __init__(self):
        self.logger = current_app.logger

        self.notification_type_service = NotificationTypeService()

    def get(self, notification_type_id: int):
        try:
            notification_type_model = self.notification_type_service.get_by_id(notification_type_id)
            return notification_type_model.to_rest()
        except BaseApiException as err:
            return err.to_rest()

        except Exception as unhandled:
            self.logger.error(f'Unhandled Error {str(type(unhandled))} was encountered')
            return BaseApiException.from_exception(unhandled).to_rest()
