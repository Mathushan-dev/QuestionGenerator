from tests.UserQuestionHandlerControllerTester import test_application
from application.controllers.UserQuestionHandlerController import create_mc_questions


def test_create_mc_questions():
    """
    GIVEN a Flask application configured for testing
    WHEN the 'create_mc_questions' method is called
    THEN check that the response is valid
    :return: None
    """
    question_id_hashes, questions, options, answers = create_mc_questions("Harry walked to the park.", "4")
    assert len(question_id_hashes) == 1
    assert len(questions) == 1
    assert len(options) == 1
    assert len(options[0]) == 4
    assert len(answers) == 1

    question_id_hashes, questions, options, answers = create_mc_questions(
        "Harry walked to the park. Harry plays with Sanjay.", "3")
    assert len(question_id_hashes) == 2
    assert len(questions) == 2
    assert len(options) == 2
    assert len(options[0]) == 3
    assert len(options[1]) == 3
    assert len(answers) == 2
