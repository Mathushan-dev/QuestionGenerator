import requests
from application import application


class UserLoginSignupControllerTester:
    flask_app = None

    def __init__(self):
        """
        todo
        """
        self.flask_app = application


test_application = UserLoginSignupControllerTester()


def test_generate_mc_question_api():
    with test_application.flask_app.test_client() as test_client:
        response = test_client.post('/generateMCQuestionAPI?context="Jack walked to the '
                                    'shop"&numberOptions=4')
        assert response.status_code == 200


def test_generate_tf_question_api():
    with test_application.flask_app.test_client() as test_client:
        response = test_client.post('/generateTFQuestionAPI?context="Jack walked to the shop"')
        assert response.status_code == 200
