from tests.UserQuestionHandlerControllerTester import test_application
from application.controllers.UserQuestionHandlerController import create_tf_questions


def test_create_tf_questions():
    """
    GIVEN a Flask application configured for testing
    WHEN the 'create_tf_questions' method is called
    THEN check that the response is valid
    :return: None
    """
    question_id_hashes, questions, options, answers = create_tf_questions("Harry walked to the park.")
    assert len(question_id_hashes) == 1
    assert len(questions) == 1
    assert len(options) == 1
    assert len(options[0]) == 2
    assert len(answers) == 1

    question_id_hashes, questions, options, answers = create_tf_questions(
        "Harry walked to the park. Jack walked to the shop with Mathushan.")
    assert len(question_id_hashes) == 2
    assert len(questions) == 2
    assert len(options) == 2
    assert len(options[0]) == 2
    assert len(options[1]) == 2
    assert len(answers) == 2