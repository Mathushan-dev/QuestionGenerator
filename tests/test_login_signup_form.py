from tests.UserLoginSignupControllerTester import test_application


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
