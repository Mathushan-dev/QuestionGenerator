from tests.UserQuestionHandlerControllerTester import test_application
from application.controllers.UserQuestionHandlerController import save_current_questions


def test_save_current_questions():
    """
    GIVEN a Flask application configured for testing
    WHEN the 'save_current_questions' method is called
    THEN check that the response is valid
    :return: None
    """
    current_question_id_hashes, current_questions, current_options, current_answers, current_context, current_question_set_code = save_current_questions()
    assert current_question_id_hashes == "test_question_id_hashes"
    assert current_questions == "test_questions"
    assert current_options == "test_options"
    assert current_answers == "test_answers"
    assert current_context == "test_context"
    assert current_question_set_code == "test_question_set_code"
