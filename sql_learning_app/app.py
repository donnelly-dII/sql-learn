from flask import Blueprint
from flask_restful import Api

# Import Resources
from .api_vi.hello import HelloResource, HelloMessageResource, HelloMessageIdResource
from sql_learning_app.api_vi.entity.user.person import PersonResource, PersonIdResource
from .api_vi.admin.notification_type import NotificationTypeResource, NotificationTypeIdResource
from .api_vi.entity.notification import NotificationResource


api_bp = Blueprint("api", __name__)
api = Api(api_bp)

# Hello World Resources
api.add_resource(HelloResource, '/hello')
api.add_resource(HelloMessageResource, '/hello/message')
api.add_resource(HelloMessageIdResource, '/hello/message/<int:hello_id>')

#
# ADMIN RESOURCES / ENDPOINTS
#

# Notification Type Resources
api.add_resource(NotificationTypeResource, '/admin/notificationtype')
api.add_resource(NotificationTypeIdResource, '/admin/notificationtype/<int:notification_type_id>')

#
# ENTITY RESOURCES / ENDPOINTS
#

# Person Resources
api.add_resource(PersonResource, '/person')
api.add_resource(PersonIdResource, '/person/<int:person_id>')

# Notification Resources
api.add_resource(NotificationResource, '/notification')
