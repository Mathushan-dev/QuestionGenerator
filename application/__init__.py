from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application.models.UserLoginSignupModel import db

# Globally accessible libraries
db = SQLAlchemy()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialise Plugins
    db.init_app(app)

    with app.app_context():
        # Include our Routes
        from application.routes.UserLoginSignupBP import UserLoginSignupBP
        from application.routes.UserQuestionHandlerBP import UserQuestionHandlerBP

        # Register Blueprints
        app.register_blueprint(UserLoginSignupBP)
        app.register_blueprint(UserQuestionHandlerBP)

        return app
