from tests.UserAPIControllerTester import test_application


def test_generate_mc_question_api():
    with test_application.flask_app.test_client() as test_client:
        response = test_client.post('/generateMCQuestionAPI?context="Jack walked to the '
                                    'shop"&numberOptions=4')
        assert response.status_code == 200
