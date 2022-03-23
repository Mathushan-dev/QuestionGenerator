from app import app


class UserLoginSignupControllerTester:
    flask_app = None

    def __init__(self):
        """
        todo
        """
        self.flask_app = app


test_application = UserLoginSignupControllerTester()