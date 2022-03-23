from tests.UserQuestionHandlerControllerTester import test_application


def test_load_current_questions():
    """
    GIVEN a Flask application configured for testing
    WHEN the 'load_current_questions' method is called
    THEN check that the response is valid
    :return: None
    """
    with test_application.flask_app.test_client() as test_client:
        response = test_client.get('/loadCurrentQuestions')
        assert b'Question' in response.data
