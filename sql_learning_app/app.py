from flask import Blueprint
from flask_restful import Api

# Import Resources
from .api_vi.hello import HelloResource, HelloMessageResource, HelloMessageIdResource

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

# Hello World Resources
api.add_resource(HelloResource, '/hello')
api.add_resource(HelloMessageResource, '/hello/message')
api.add_resource(HelloMessageIdResource, '/hello/message/<int:hello_id>')
