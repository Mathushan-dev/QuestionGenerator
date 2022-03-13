from application import application
from controllers.UserQuestionHandlerController import save_current_questions, \
    create_tf_questions, create_mc_questions


class UserLoginSignupControllerTester:
    flask_app = None

    def __init__(self):
        """
        todo
        """
        self.flask_app = application


test_application = UserLoginSignupControllerTester()


# def test_add_question_to_database():
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the 'add_question_to_database' method is called
#     THEN check that the response is valid
#     :return: None
#     """
#     question = test_application.flask_app.add_question_to_database()
#     assert question.questionId == "test_question_id"
#     assert question.context == "test_question_context"
#     assert question.question == "test_question"
#     assert question.answer == "test_answer"
#     assert question.options == "test_options"
#     assert question.questionNumber == "test_question_number"
#     assert question.questionSetCode == "test_question_set_code"


def test_save_current_questions():
    """
    GIVEN a Flask application configured for testing
    WHEN the 'save_current_questions' method is called
    THEN check that the response is valid
    :return: None
    """
    current_question_id_hashes, current_questions, current_options, current_answers, current_context = save_current_questions()
    assert current_question_id_hashes == "test_question_id_hashes"
    assert current_questions == "test_questions"
    assert current_options == "test_options"
    assert current_answers == "test_answers"
    assert current_context == "test_context"


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


def test_generate_tf_questions():
    """
    GIVEN a Flask application configured for testing
    WHEN the 'generate_tf_questions' method is called
    THEN check that the response is valid
    :return: None
    """
    with test_application.flask_app.test_client() as test_client:
        response = test_client.get('/generateTFQuestions')
        assert b'Question' in response.data


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


def test_generate_mc_questions():
    """
    GIVEN a Flask application configured for testing
    WHEN the 'generate_mc_questions' method is called
    THEN check that the response is valid
    :return: None
    """
    with test_application.flask_app.test_client() as test_client:
        response = test_client.get('/generateMCQuestions')
        assert b'Question' in response.data


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
