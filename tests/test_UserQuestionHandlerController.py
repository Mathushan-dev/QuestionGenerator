from application import application
from controllers.UserQuestionHandlerController import add_question_to_database, save_current_questions, \
    load_current_questions
from models.UserQuestionHandlerModel import UserQuestionHandler


class UserLoginSignupControllerTester:
    flask_app = None

    def __init__(self):
        """
        todo
        """
        self.flask_app = application


test_application = UserLoginSignupControllerTester()


def test_add_question_to_database():
    """
    GIVEN a Flask application configured for testing
    WHEN the 'add_question_to_database' method is called
    THEN check that the response is valid
    :return: None
    """
    question = add_question_to_database()
    assert question.questionId == "test_question_id"
    assert question.context == "test_question_context"
    assert question.question == "test_question"
    assert question.answer == "test_answer"
    assert question.options == "test_options"
    assert question.questionNumber == "test_question_number"
    assert question.questionSetCode == "test_question_set_code"


def test_save_current_questions():
    """
    GIVEN a Flask application configured for testing
    WHEN the 'save_current_questions' method is called
    THEN check that the response is valid
    :return: None
    """
    currentQuestionIdHashes, currentQuestions, currentOptions, currentAnswers, currentContext = save_current_questions()
    assert currentQuestionIdHashes == "test_question_id_hashes"
    assert currentQuestions == "test_questions"
    assert currentOptions == "test_options"
    assert currentAnswers == "test_answers"
    assert currentContext == "test_context"


def test_load_current_questions():
    """
    GIVEN a Flask application configured for testing
    WHEN the 'load_current_questions' method is called
    THEN check that the response is valid
    :return: None
    """
    response = load_current_questions("mcq")
    assert b'Question' in response
    response = load_current_questions("tf")
    assert b'Question' in response


def test_generate_tf_questions():
    """
    GIVEN a Flask application configured for testing
    WHEN the 'generate_tf_questions' method is called
    THEN check that the response is valid
    :return: None
    """
    response = load_current_questions("mcq")
    assert b'Question' in response
    response = load_current_questions("tf")
    assert b'Question' in response


def test_sign_up():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signUp' page is requested (GET)
    THEN check that the response is valid
    :return: None
    """
    with test_application.flask_app.test_client() as test_client:
        response = test_client.post('/signUp')
        assert response.status_code == 200
        assert b'Enter a passage!' in response.data
        assert b'Number of options:' in response.data


def test_log_in():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/logIn' page is requested (GET)
    THEN check that the response is valid
    :return: None
    """
    with test_application.flask_app.test_client() as test_client:
        test_client.post('/signUp')
        test_client.post('/')
        response = test_client.post('/logIn')
        assert response.status_code == 200
        assert b'Enter a passage!' in response.data
        assert b'Number of options:' in response.data


def test_log_out():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/logOut' page is requested (GET)
    THEN check that the response is valid
    :return: None
    """
    with test_application.flask_app.test_client() as test_client:
        test_client.post('/signUp')
        test_client.post('/')
        response = test_client.post('/logOut')
        assert response.status_code == 200
        assert b'Enter a passage!' in response.data
        assert b'Number of options:' in response.data


def test_load_home():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/loadHome' page is requested (GET)
    THEN check that the response is valid
    :return: None
    """
    with test_application.flask_app.test_client() as test_client:
        test_client.post('/signUp')
        response = test_client.post('/loadHome')
        assert response.status_code == 200
        assert b'Edit' in response.data
        assert b'Your progress' in response.data


def test_delete_account():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/deleteAccount' page is requested (GET)
    THEN check that the response is valid
    :return: None
    """
    with test_application.flask_app.test_client() as test_client:
        test_client.post('/signUp')
        response = test_client.post('/deleteAccount')
        assert response.status_code == 200
        assert b'X5LEARN' in response.data
        assert b'Why choose X5Learn?' in response.data


def test_stringify_list():
    """
    GIVEN a list configured for testing
    WHEN the 'stringify_list' method is called
    THEN check that the result is valid
    :return: None
    """
    assert stringify_list(["test", "test"]).strip() == "test,test"
    assert stringify_list([]).strip() == ""
    assert stringify_list(["test"]).strip() == "test"
    assert stringify_list(["test", "test", "test"]).strip() == "test,test,test"


def test_update_record():
    """
    GIVEN a UserLoginSignup configured for testing
    WHEN the 'update_records' method is called
    THEN check that the result is valid
    :return: None
    """
    user = UserLoginSignup("test@test.test", "test_first_name", "test_last_name",
                           hashed_password=UserLoginSignup.make_password_hash("test_password"))

    a, b, c, d, e = update_records(user, "test_question_id_hash", "test_score", "test_tries")
    assert "test_question_id_hash" in a
    assert "test_score" in b
    assert "test_tries" in c

    user.attemptedQuestionIds = "test_question_id_hash"
    user.questionScores = "test_score"
    user.numberOfAttempts = "test_tries"
    a, b, c, d, e = update_records(user, "test_question_id_has2h", "test_scor2e", "test_trie2s")
    assert "test_question_id_hash" in a
    assert "test_score" in b
    assert "test_tries" in c
    assert "test_question_id_has2h" in a
    assert "test_scor2e" in b
    assert "test_trie2s" in c

    user.attemptedQuestionIds = "test_question_id_hash,test_question_id_has2h"
    user.questionScores = "test_score,test_scor2e"
    user.numberOfAttempts = "test_tries,test_trie2s"
    a, b, c, d, e = update_records(user, "test_question_id_hash", "test_scorne", "test_triens")
    assert "test_question_id_hash" in a
    assert "test_score" not in b
    assert "test_tries" not in c
    assert "test_question_id_hash" in a
    assert "test_scorne" in b
    assert "test_triens" in c
    assert "test_question_id_has2h" in a
    assert "test_scor2e" in b
    assert "test_trie2s" in c


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
        assert b'Show Text' in response.data
