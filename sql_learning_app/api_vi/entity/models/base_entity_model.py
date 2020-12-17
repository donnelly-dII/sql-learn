#
# To imlement Table Inheritance for our Users that can be people, Universities, or Organizations
# We need to create the base entity model class that can put all IDs in single spot with base information
# Like username, date started, and other shared data
#
from datetime import datetime
from marshmallow import Schema, fields, post_load, ValidationError

# Local imports
from sql_learning_app.config import db
from sql_learning_app.api_vi.common import InvalidRequest


class EntityModel:

    def __init__(self):
        pass


class EntityDBModel(db.Model):
    __tablename__ = 'Entity'
    entity_id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False)
