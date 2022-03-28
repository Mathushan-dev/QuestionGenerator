from tests.UserLoginSignupControllerTester import test_application


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
        assert b'Welcome' in response.data
        assert b'YWhy not try the 5 recent questions generated around the world?' in response.data
