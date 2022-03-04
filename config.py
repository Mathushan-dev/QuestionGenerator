import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = False
# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://vczoqebk:Xyf9h4SyYkWYyeSYu3N9oE4wqIloAYI7@jelani.db.elephantsql.com/vczoqebk'
# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
