from flask import Flask, render_template
from flask_migrate import Migrate
from models.UserLoginSignupModel import db
from routes.UserLoginSignupBP import UserLoginSignupBP
from routes.UserQuestionHandlerBP import UserQuestionHandlerBP
from config import DEBUG

application = Flask(__name__)
application.config.from_object('config')
db.init_app(application)
migrate = Migrate(application, db)
application.register_blueprint(UserLoginSignupBP)
application.register_blueprint(UserQuestionHandlerBP)


@application.route('/')
def index():
    return render_template('launchpage.html')


if __name__ == '__main__':
    application.debug = DEBUG
    application.run(host='0.0.0.0')
    db.create_all()
