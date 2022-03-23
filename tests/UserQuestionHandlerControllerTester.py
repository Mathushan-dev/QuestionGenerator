from wsgi import app


class UserQuestionHandlerControllerTester:
    flask_app = None

    def __init__(self):
        """
        todo
        """
        self.flask_app = app


test_application = UserQuestionHandlerControllerTester()
