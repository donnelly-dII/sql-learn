#
#  API controller for Person ID Resource
#

from flask_restful import Resource
from flask import current_app, request
from marshmallow import ValidationError

# Internal packages
from ..models import PersonRestModel
from ..person_service import PersonService

# Internal Exceptions
from sql_learning_app.api_vi.common import BaseApiException, InvalidRequest


class PersonIdResource(Resource):

    def __init__(self):
        self.logger = current_app.logger

        self.person_serializer = PersonRestModel()
        self.person_service = PersonService()

    def get(self, person_id: int):
        """GET a person object by ID
        :param person_id: DB ID of person
        :return: Person object
        """
        try:
            return self.person_service.fetch_by_id(person_id).to_rest()
        except BaseApiException as err:
            return err.to_rest()
        except Exception as general_err:
            self.logger.critical(f'UNhandled Error {general_err} was encountered while attempting to fetch '
                                 f'Person entity with ID {person_id}')
            return BaseApiException.from_exception(general_err).to_rest()
