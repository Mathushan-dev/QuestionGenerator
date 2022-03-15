from wsgi import app
from application.controllers.UserLoginSignupController import stringify_list, update_records
from application.models.UserLoginSignupModel import UserLoginSignup


class UserLoginSignupControllerTester:
    flask_app = None

    def __init__(self):
        """
        todo
        """
        self.flask_app = app


test_application = UserLoginSignupControllerTester()


def test_index():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    :return: None
    """
    with test_application.flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b'X5LEARN' in response.data
        assert b'Why choose X5Learn?' in response.data


def test_login_signup_form():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/loginForm' page is requested (GET)
    THEN check that the response is valid
    :return: None
    """
    with test_application.flask_app.test_client() as test_client:
        response = test_client.get('/loginForm')
        assert response.status_code == 200
        assert b'Sign Up' in response.data
        assert b'Log In' in response.data


def test_load_enter_text():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/enterText' page is requested (GET)
    THEN check that the response is valid
    :return: None
    """
    with test_application.flask_app.test_client() as test_client:
        response = test_client.get('/enterText')
        assert response.status_code == 200
        assert b'Enter a passage!' in response.data
        assert b'Number of options:' in response.data


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
