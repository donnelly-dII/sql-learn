#
#   General Exception for an Invalid Payload request from client
#

from marshmallow import ValidationError

# Third party modules
from .base_exception import BaseApiException


class InvalidRequest(BaseApiException):

    def __init__(self, error: ValidationError, endpoint: str = None):
        """Constructor for InvalidRequest
        :param error: Marshmallow InvalidError
        :param endpoint: optional API endpoint to include in message
        """
        msg = 'Invalid Payload Request'
        if endpoint:
            msg += f' to endpoint {endpoint}'
        msg += f'. The following parameters had issues: {str(error.messages)}'
        super().__init__(msg)
        self.status_code = 400
