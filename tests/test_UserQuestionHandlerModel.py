from application.models.UserQuestionHandlerModel import UserQuestionHandler


def test_new_user_question_handler():
    """
    GIVEN a UserQuestionHandler model
    WHEN a new question is created
    THEN check the questionId, context,
    question, answer, options, questionNumber
    and questionSetCode fields are defined
    correctly
    :return: None
    """

    question = UserQuestionHandler(UserQuestionHandler.make_question_id_hash("test_question_id"), "test_context",
                                   "test_question", "test_answer", "test_options", "test_question_number",
                                   "test_question_set_code")
    assert question.questionId != "test_question_id"
    assert question.is_question_id_match("test_question_id")
    assert question.context == "test_context"
    assert question.question == "test_question"
    assert question.answer == "test_answer"
    assert question.options == "test_options"
    assert question.questionNumber == "test_question_number"
    assert question.questionSetCode == "test_question_set_code"
