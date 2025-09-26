from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema
from marshmallow_sqlalchemy import SQLAlchemySchema
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Schema
jwt = JWTManager()
