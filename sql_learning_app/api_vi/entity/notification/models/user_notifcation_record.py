#
# Helper Rest class for UserNotifications
#

from marshmallow import Schema, fields, post_load, ValidationError

# Local imports
from sql_learning_app.config import db
from sql_learning_app.api_vi.common import InvalidRequest


class UserNotificationRecordRestModel(Schema):
    message = fields.String()



class UserNotificationRecord:
    pass
