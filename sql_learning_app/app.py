from flask import Blueprint
from flask_restful import Api

# Import Resources
from .api_vi.hello import HelloResource, HelloMessageResource, HelloMessageIdResource
from .api_vi.notification_type import NotificationTypeResource, NotificationTypeIdResource

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

# Hello World Resources
api.add_resource(HelloResource, '/hello')
api.add_resource(HelloMessageResource, '/hello/message')
api.add_resource(HelloMessageIdResource, '/hello/message/<int:hello_id>')

# Notification Type Resources
api.add_resource(NotificationTypeResource, '/notificationtype')
api.add_resource(NotificationTypeIdResource, '/notificationtype/<int:notification_type_id>')
