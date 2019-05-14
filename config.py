import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' +  os.path.join(basedir, 'database.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
