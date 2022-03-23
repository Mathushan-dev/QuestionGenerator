from tests.UserLoginSignupControllerTester import test_application


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
