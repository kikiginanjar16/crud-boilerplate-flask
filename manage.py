from app import create_app
from flask_migrate import Migrate
from app.extensions import db
from app import models

app=create_app(); migrate=Migrate(app, db)
