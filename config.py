import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = 'postgres://vczoqebk:Xyf9h4SyYkWYyeSYu3N9oE4wqIloAYI7@jelani.db.elephantsql.com/vczoqebk'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = 'production'
    DEBUG = False
    TEST = False
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
