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


class HelloMessageResource(Resource):

    def __init__(self):
        self.logger = current_app.logger

        self.hello_serializer = HelloRestModel()
        self.hello_service = HelloMessageService()

    def get(self):
        """GET operation to fetch all Hello World messages
        :return: List of all the records
        """
        pass

    def post(self):
        """POST to create a new Hello Message
        :return: Hello Object that is created
        """
        try:
            data = request.get_json()
            hello_model = self.hello_serializer.load(data)
        except ValidationError as err:
            return InvalidRequest(err).to_rest()

        # Create a new Hello Message with this model
        try:
            return self.hello_service.create_new_hello_msg(hello_model).to_rest()
        except BaseApiException as internal_err:
            self.logger.error(f'Hello creation failed with the error: {internal_err}')
            return internal_err.to_rest()
        except Exception as general_err:
            self.logger.error(f'Hello creation failed with the error: {general_err}')
            return BaseApiException.from_exception(general_err).to_rest()
