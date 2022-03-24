from application.models.UserLoginSignupModel import UserLoginSignup
from application.models.UserQuestionHandlerModel import UserQuestionHandler
from application.models.UserLoginSignupModel import db


def get_total_right_wrong(question_scores):
    """
    :param question_scores: score of the question
    :return: number of right questions, number of wrong questions
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


def get_individual_test_summary(attempted_question_ids, question_scores, number_of_attempts, attempted_dates):
    """
    This method provides the individual summary of attempting questions
    :param attempted_question_ids: attempted question ids
    :param question_scores: score of the question
    :param number_of_attempts: number of attempts
    :return: questions, contexts, options , question scores and number of attempts
    """
    attempted_question_ids_split = attempted_question_ids.split(",")
    questions_split = []
    contexts_split = []
    options_split = []

    for questionId in attempted_question_ids_split:
        if questionId.strip() != "":
            questions = db.session.query(UserQuestionHandler).filter(UserQuestionHandler.questionId == questionId).all()
            db.session.commit()
            questions_split.append(questions[0].question)
            contexts_split.append(questions[0].context)
            options_split.append(questions[0].options)

    question_scores_split = question_scores.split(",")
    number_of_attempts_split = number_of_attempts.split(",")
    attempted_dates_split = attempted_dates.split(",")

    return questions_split, contexts_split, options_split, question_scores_split, number_of_attempts_split, attempted_dates_split


def get_profile_stats(user_id):
    """
    This method gets the statistics of the user
    :param user_id: user id in database
    :return: first and last name of user, total right and wrong number, questions, contexts,options,
    scores and attempts
    """
    users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId == user_id).all()
    db.session.commit()

    first_name, last_name = users[0].fName, users[0].lName
    try:
        questions, contexts, options, scores, attempts, dates = get_individual_test_summary(users[0].attemptedQuestionIds, users[0].questionScores,
                                                                                 users[0].numberOfAttempts, users[0].attemptedDates)
        total_right, total_wrong = get_total_right_wrong(users[0].questionScores)
    except IndexError:
        return first_name, last_name, 0, 0, [], [], [], [], [], []

    return first_name, last_name, total_right, total_wrong, questions, contexts, options, scores, attempts, dates
