from flask import current_app
from flask_restful import Resource


class HelloResource(Resource):

    def __init__(self):
        self.logger = current_app.logger

    def get(self):
        # Fetch the user
        self.logger.info(f'Hello World Request made by User {"temp"}')
        return "Hello, World!"
