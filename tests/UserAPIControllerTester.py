from wsgi import app


class UserAPIControllerTester:
    flask_app = None

    def __init__(self):
        """
        todo
        """
        self.flask_app = app


test_application = UserAPIControllerTester()