from tests.UserLoginSignupControllerTester import test_application


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
