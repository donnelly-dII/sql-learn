#
#  API controller for HelloMessage resource
#

from flask_restful import Resource
from flask import current_app, request
from marshmallow import ValidationError

# Internal packages
from ..models import HelloRestModel
from ..service import HelloMessageService

# Internal Exceptions
from sql_learning_app.api_vi.common import BaseApiException, InvalidRequest


class HelloMessageIdResource(Resource):

    def __init__(self):

        self.logger = current_app.logger
        self.service = HelloMessageService()

    def get(self, hello_id: int):
        """GET by specific ID
        :param hello_id: hello_id of message
        :return: HelloModel object
        """
        try:
            model = self.service.get_by_id(hello_id)
            self.logger.info(f'Successfully fetched Hello object with ID {id}')
            return model.to_rest()
        except BaseApiException as err:
            return err.to_rest()
        except Exception as unhandled:
            return BaseApiException.from_exception(unhandled).to_rest()
