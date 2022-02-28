from models.UserLoginSignupModel import UserLoginSignup
from models.UserQuestionHandlerModel import UserQuestionHandler
from models.UserLoginSignupModel import db


def getTotalRightWrong(questionScores):
    questionScoresSplit = questionScores.split(",")
    totalRight = 0
    totalWrong = 0
    for score in questionScoresSplit:
        if score == "1":
            totalRight += 1
        if score == "0":
            totalWrong += 1
    return totalRight, totalWrong


def getIndividualTestSummary(attemptedQuestionIds, questionScores, numberOfAttempts):
    attemptedQuestionIdsSplit = attemptedQuestionIds.split(",")
    questionsSplit = []
    contextsSplit = []
    optionsSplit = []

    for questionId in attemptedQuestionIdsSplit:
        if questionId.strip() != "":
            questions = db.session.query(UserQuestionHandler).filter(UserQuestionHandler.questionId == questionId).all()
            db.session.flush()
            questionsSplit.append(questions[0].question)
            contextsSplit.append(questions[0].context)
            optionsSplit.append(questions[0].options)

    questionScoresSplit = questionScores.split(",")
    numberOfAttemptsSplit = numberOfAttempts.split(",")

    return questionsSplit, contextsSplit, optionsSplit, questionScoresSplit, numberOfAttemptsSplit


def getProfileStats(userId):
    users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId == userId).all()
    db.session.flush()

    firstName, lastName = users[0].fName, users[0].lName
    questions, contexts, options, scores, attempts = getIndividualTestSummary(users[0].attemptedQuestionIds, users[0].questionScores,
                                                           users[0].numberOfAttempts)
    totalRight, totalWrong = getTotalRightWrong(users[0].questionScores)

    return firstName, lastName, totalRight, totalWrong, questions, contexts, options, scores, attempts
