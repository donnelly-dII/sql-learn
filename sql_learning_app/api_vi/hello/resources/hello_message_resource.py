from flask import current_app, request
from flask_restful import Resource

from ..models import HelloRestModel
from ..service import HelloMessageService


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
        data = request.get_json()
        hello_model = self.hello_serializer.load(data)

        # Create a new Hello Message with this model
        try:
            return self.hello_service.create_new_hello_msg(hello_model).to_rest()
        except Exception as general_err:
            pass
        pass


