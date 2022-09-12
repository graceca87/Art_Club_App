from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os


app = Flask(__name__)
app.config.from_object(Config)

IMG_FOLDER = os.path.join('static', 'IMG')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

# Create an instance of SQLAlchemy (the ORM) with the Flask Application
db = SQLAlchemy(app)
# Create an instance of Migrate which will be our migration engine and pass in the app and SQLAlchemy instance
migrate = Migrate(app, db)
# render_as_batch=True
# Create an instance of the LoginManager to handle authentication
login = LoginManager(app)
login.login_view = 'login' # Tells login manager which enpoint to redirect if not logged in
login.login_message = 'You must be logged in to view or edit addresses, you silly goose!'
login.login_category = 'danger'


from . import routes, models
