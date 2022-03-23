from tests.UserAPIControllerTester import test_application


def test_generate_tf_question_api():
    with test_application.flask_app.test_client() as test_client:
        response = test_client.post('/generateTFQuestionAPI?context="Jack walked to the shop"')
        assert response.status_code == 200
