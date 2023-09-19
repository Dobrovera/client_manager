from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS

from facility_management.settings import *


app = Flask(__name__)
cors = CORS(app)
app.secret_key = SECRET_KEY
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)
manager = LoginManager(app)
migrate = Migrate(app, db)
app.app_context().push()

from facility_management import models, routes, nsis_routes, object_routes
