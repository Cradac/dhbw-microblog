from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very-secret-key'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
loginMgr = LoginManager(app)

from app import routes, models
