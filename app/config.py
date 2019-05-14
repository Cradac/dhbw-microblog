import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'