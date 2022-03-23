from tests.UserLoginSignupControllerTester import test_application


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
