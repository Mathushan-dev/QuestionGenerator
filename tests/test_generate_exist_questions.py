from tests.UserQuestionHandlerControllerTester import test_application


def test_generate_exist_questions():
    """
    GIVEN a Flask application configured for testing
    WHEN the 'generate_exist_questions' method is called
    THEN check that the response is valid
    :return: None
    """
    with test_application.flask_app.test_client() as test_client:
        response = test_client.get('/generateExistQuestions')
        assert b'Number of options:' in response.data
        # The test below can only be used if a question with the question code below exits in the database
        # response = generate_exist_questions(question_set_code)
        # assert b'Question' in response
