#
#   Base Error to be used across API for proper error payload serialization
#
import traceback


class BaseApiException(Exception):

    def __init__(self, msg: str):
        """Constructor for the base API error class
        :param msg: Error message
        """
        super().__init__()
        self.status_code = 500
        self.message = msg
        self.error_name = type(self).__name__
        self.error_traceback = None

    def to_rest(self) -> tuple:
        """Converts the Exception into a proper API response
        :return: tuple in proper format for REST
        """
        return_payload = {'error': str(self.error_name), 'message': str(self.message)}

        # Append Traceback if has it
        if self.error_traceback:
            return_payload['traceback'] = self.error_traceback

        return return_payload, self.status_code

    @classmethod
    def from_exception(cls, error: Exception) -> 'BaseApiException':
        """Creates an instance of the Base error from a general python exception.
            To be used for unhandled internal errors and still ensuring proper REST response
        :param error: unhandled python Exception
        :return: The BaseApiException created from the general one
        """
        msg = f'An unhandled error of type {type(error)} was encountered on the server with the following details: '
        handled_exception = BaseApiException(msg)

        # Set attributes from error
        handled_exception.error_name = error.__class__
        handled_exception.error_traceback = traceback.format_exc().splitlines()

        return handled_exception
