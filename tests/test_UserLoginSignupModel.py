from application.models.UserLoginSignupModel import UserLoginSignup


def test_new_user_login_signup():
    """
    GIVEN a UserLoginSignup model
    WHEN a new user is created
    THEN check the userId, fName, lName,
    hashedPassword, attemptedQuestionIds,
    questionScores, numberOfAttempts,
    attemptedDates and attemptedTimes fields
    are defined correctly
    :return: None
    """

    user = UserLoginSignup("test@test.test", "test_first_name", "test_last_name",
                           hashed_password=UserLoginSignup.make_password_hash("test_password"))
    assert user.userId == "test@test.test"
    assert user.fName == "test_first_name"
    assert user.lName == "test_last_name"
    assert user.hashedPassword != "test_password"
    assert user.is_password_valid("test_password")
    assert user.attemptedQuestionIds == ""
    assert user.questionScores == ""
    assert user.numberOfAttempts == ""
    assert user.attemptedDates == ""
    assert user.attemptedTimes == ""
