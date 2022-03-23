from tests.UserLoginSignupControllerTester import test_application


def test_save_question_attributes():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/saveQuestionAttributes' page is requested (GET)
    THEN check that the response is valid
    :return: None
    """
    with test_application.flask_app.test_client() as test_client:
        test_client.post('/signUp')
        response = test_client.post('/saveQuestionAttributes')
        assert response.status_code == 200
        assert b'Show text' in response.data
