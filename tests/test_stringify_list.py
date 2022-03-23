from tests.UserLoginSignupControllerTester import test_application
from application.controllers.UserLoginSignupController import stringify_list

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
