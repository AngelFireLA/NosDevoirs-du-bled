import os

class Config(object):
    SECRET_KEY = 'comment_es_tu_la'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False