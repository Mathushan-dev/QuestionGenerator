from models.UserLoginSignupModel import UserLoginSignup
from models.UserQuestionHandlerModel import UserQuestionHandler
from models.UserLoginSignupModel import db


def get_total_right_wrong(question_scores):
    """
    todo
    :param question_scores:
    :return: Tuple[int, int]
    """
    question_scores_split = question_scores.split(",")
    total_right = 0
    total_wrong = 0
    for score in question_scores_split:
        if score == "1":
            total_right += 1
        if score == "0":
            total_wrong += 1
    return total_right, total_wrong


def get_individual_test_summary(attempted_question_ids, question_scores, number_of_attempts):
    """
    todo
    :param attempted_question_ids:
    :param question_scores:
    :param number_of_attempts:
    :return: Tuple[list, list, list, Any, Any]
    """
    attempted_question_ids_split = attempted_question_ids.split(",")
    questions_split = []
    contexts_split = []
    options_split = []

    for questionId in attempted_question_ids_split:
        if questionId.strip() != "":
            questions = db.session.query(UserQuestionHandler).filter(UserQuestionHandler.questionId == questionId).all()
            db.session.flush()
            questions_split.append(questions[0].question)
            contexts_split.append(questions[0].context)
            options_split.append(questions[0].options)

    question_scores_split = question_scores.split(",")
    number_of_attempts_split = number_of_attempts.split(",")

    return questions_split, contexts_split, options_split, question_scores_split, number_of_attempts_split


def get_profile_stats(user_id):
    """
    todo
    :param user_id:
    :return: Tuple[Any, Any, int, int, list, list, list, Any, Any]
    """
    users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId == user_id).all()
    db.session.flush()

    first_name, last_name = users[0].fName, users[0].lName
    questions, contexts, options, scores, attempts = get_individual_test_summary(users[0].attemptedQuestionIds, users[0].questionScores,
                                                                                 users[0].numberOfAttempts)
    total_right, total_wrong = get_total_right_wrong(users[0].questionScores)

    return first_name, last_name, total_right, total_wrong, questions, contexts, options, scores, attempts
