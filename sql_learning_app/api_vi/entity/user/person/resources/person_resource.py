#
#  API controller for Person Resource
#

from flask_restful import Resource
from flask import current_app, request
from marshmallow import ValidationError

# Internal packages
from ..models import PersonRestModel
from ..person_service import PersonService

# Internal Exceptions
from sql_learning_app.api_vi.common import BaseApiException, InvalidRequest


class PersonResource(Resource):

    def __init__(self):
        self.logger = current_app.logger

        self.person_serializer = PersonRestModel()
        self.person_service = PersonService()

    def get(self):
        """GET operation to fetch all Hello World messages
        :return: List of all the records
        """
        pass

    def post(self):
        """POST to create a new Person object
        :return: Person Object that is created
        """
        try:
            data = request.get_json()
            person = self.person_serializer.load(data)
        except ValidationError as err:
            return InvalidRequest(err).to_rest()

        # Create a new Hello Message with this model
        try:
            return self.person_service.create_new_person(person).to_rest()
        except BaseApiException as internal_err:
            self.logger.error(f'Hello creation failed with the error: {internal_err}')
            return internal_err.to_rest()
        except Exception as general_err:
            self.logger.error(f'Hello creation failed with the error: {general_err}')
            return BaseApiException.from_exception(general_err).to_rest()
