from flask import Flask, render_template
from flask_migrate import Migrate
from models.UserLoginSignupModel import db
from routes.UserLoginSignupBP import UserLoginSignupBP
from routes.UserQuestionHandlerBP import UserQuestionHandlerBP
from config import DEBUG

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(UserLoginSignupBP)
app.register_blueprint(UserQuestionHandlerBP)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = DEBUG
    app.run()