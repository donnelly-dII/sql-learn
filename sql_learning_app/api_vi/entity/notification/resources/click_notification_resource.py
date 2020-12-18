#
# click_notification_resource offers theendpoint and API resource for when a user clicks a NotificationRecord
#

from flask_restful import Resource
from flask import current_app, redirect, url_for, Response
from marshmallow import ValidationError

# Internal packages
from ..models import NotificationRestModel
from sql_learning_app.api_vi.entity.notification.services.notification_record_service import NotificationRecordService

# Internal Exceptions
from sql_learning_app.api_vi.common import BaseApiException, InvalidRequest

URI = '/click/notification'


class ClickNotificationResource(Resource):

    def __init__(self):
        self.logger = current_app.logger

        self.record_service = NotificationRecordService()

    def get(self, notification_record_id):
        """Redirect the notification click to the proper entity page
        :param notification_record_id: notification_record_id of notification recordd
        """
        try:
            redirect_url = self.record_service.fetch_redirect_url(notification_record_id)
            return redirect(f'http://0.0.0.0:5000{redirect_url}', 302)

        except BaseApiException as err:
            self.logger.error(f'Failed to Notification click redirect with error: {err}')
            return err.to_rest()
        except Exception as general_err:
            self.logger.critical(f'Failed to Notification click redireect with unhandled error {general_err}')
            return BaseApiException.from_exception(general_err).to_rest()

