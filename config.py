from flask import Flask
from flask_restful import Api
from flask_security import Security
from database.db import db
import os
from datetime import timedelta
from models.models import user_datastore


class appConfiguration():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:<pass>@localhost:5432/FarmEase'
    SECURITY_PASSWORD_SALT = "12345"
    DEBUG = True

def create_app():
    app = Flask(__name__)
    app.config.from_object(appConfiguration)
    api = Api(app)
    app.app_context().push()
    app.secret_key = os.urandom(36)
    db.init_app(app)
    return app, api


app, api = create_app()

app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'wav', 'mp3'}
app.config['IMAGE_UPLOADS_PATH'] = '/static/uploads/images/'
app.config['AUDIO_UPLOADS_PATH'] = '/static/uploads/audio/'

app_security = Security(app, user_datastore)
