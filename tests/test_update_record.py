from tests.UserLoginSignupControllerTester import test_application
from application.controllers.UserLoginSignupController import update_records
from application.models.UserLoginSignupModel import UserLoginSignup


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
