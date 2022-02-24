from flask import render_template, request
from models.UserLoginSignupModel import UserLoginSignup
from controllers.UserQuestionHandlerController import loadCurrentQuestions
from functions.profileStatsCalculator import getProfileStats
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from config import DEBUG
import json

db = SQLAlchemy()

LoggedOnUserId = None
firstLaunch = True


def index():
    if DEBUG:
        print("index called")
        global firstLaunch
        if firstLaunch:
            clearTable()
            firstLaunch = False
    loggedOn = 1
    global LoggedOnUserId
    if LoggedOnUserId is None:
        loggedOn = 0
    return render_template('launchpage.html', loggedOn=loggedOn)


def loginSignupForm(message=""):
    if DEBUG:
        print("loginForm called", message)
    return render_template('signup-login.html', loginErrorMessage=message)


def loadEnterText():
    if DEBUG:
        print("try-input-passage page called")
    loggedOn = 1
    global LoggedOnUserId
    if LoggedOnUserId is None:
        loggedOn = 0
    return render_template('try-input-passage.html', loggedOn=loggedOn)


def signUp():
    if DEBUG:
        print("signUp called")
    userId = request.form.get("email")  # todo assuming email is valid in the frontend
    fName = request.form.get("fName")  # todo assuming fName is valid in the frontend
    lName = request.form.get("lName")  # todo assuming lName is valid in the frontend
    password = request.form.get("password")  # todo assuming passwordHash is strong in the frontend

    passwordHash = UserLoginSignup.makePasswordHash(password)
    user = UserLoginSignup(userId, fName, lName, passwordHash)

    try:
        db.session.add(user)
        db.session.flush()
    except IntegrityError as e:
        print(e)
        db.session.rollback()
        db.session.flush()
        return loginSignupForm(message="Those records already exist on the server, please log in instead.")
    db.session.commit()
    db.session.flush()
    global LoggedOnUserId
    LoggedOnUserId = userId
    return loadEnterText()


def logIn():
    if DEBUG:
        print("logIn called")
    userId = request.form.get("email")  # todo assuming email is valid in the frontend
    password = request.form.get("password")  # todo assuming password is strong in the frontend

    users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId == userId).all()
    db.session.flush()

    if len(users) == 0:
        return loginSignupForm(message="Those records do not exist on the server, please sign up instead.")
    elif len(users) != 1:
        return loginSignupForm(message="The server is currently down. Please try logging in later.")
        # This should never happen and something has gone terribly wrong if duplicate emails exist on database
    else:
        if users[0].isPasswordValid(password):
            global LoggedOnUserId
            LoggedOnUserId = userId
            return loadHome()  # todo change to user homepage
        return loginSignupForm(message="The password is incorrect.")


def logOut():
    if DEBUG:
        print("logOut called")
    global LoggedOnUserId
    LoggedOnUserId = None
    return index()


def loadHome():
    if DEBUG:
        print("logIn called")

    global LoggedOnUserId

    if LoggedOnUserId is None:
        return loginSignupForm("Please login or sign up for an account before viewing question results.")

    userId = LoggedOnUserId

    users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId == userId).all()
    db.session.flush()

    if len(users) != 1:
        return loginSignupForm(message="The server is currently down. Please try logging in later.")
        # This should never happen and something has gone terribly wrong if duplicate emails exist on database
    else:
        fName, lName, totalRight, totalWrong, questions, contexts, options, scores, attempts = getProfileStats(userId)
        return render_template('profile.html', fName=fName, lName=lName, totalRight=totalRight, totalWrong=totalWrong,
                               questions=questions, contexts=contexts, options=options, scores=scores,
                               attempts=attempts, loggedOn=1)


def updatePassword():
    pass


def deleteAccount():
    users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId == userId).all()
    db.session.flush()
    if len(users) == 0:
        # todo the account does not exist, so it may have been deleted already
        return index()
    elif len(users) != 1:
        return loginSignupForm(message="The server is currently down. Please try logging in later.")
        # This should never happen and something has gone terribly wrong if duplicate emails exist on database
    else:
        global LoggedOnUserId
        LoggedOnUserId = None
        try:
            stackTrace = db.session.delete(users[0])
            db.session.flush()
        except:
            print(stackTrace)
        return index()


def stringifyList(list):
    output = ""
    for i in range(0, len(list)):
        element = str(list[i])
        if element.strip() == "":
            continue
        output += str(element)
        if i == len(list) - 1:
            break
        output += ","
    return output


def updateRecords(user, questionIdHash, score, tries):
    attemptedQuestionIds = user.attemptedQuestionIds.split(",")
    questionScores = user.questionScores.split(",")
    numberOfAttempts = user.numberOfAttempts.split(",")

    for i in range(0, len(attemptedQuestionIds)):
        if attemptedQuestionIds[i].strip() == questionIdHash:
            questionScores[i] = score
            numberOfAttempts[i] = tries
            break

        if i == len(attemptedQuestionIds) - 1:
            attemptedQuestionIds.append(questionIdHash)
            questionScores.append(score)
            numberOfAttempts.append(tries)

    return stringifyList(attemptedQuestionIds), stringifyList(questionScores), stringifyList(numberOfAttempts)


def saveQuestionAttributes():
    if DEBUG:
        print("saveQuestionAttributes called")

    attributesDump = json.dumps(request.get_json())
    attributes = json.loads(attributesDump)
    questionIdHash = attributes["questionid"]
    score = attributes["score"]
    tries = attributes["tries"]

    user = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId == LoggedOnUserId).first()
    if user is not None:
        user.attemptedQuestionIds, user.questionScores, user.numberOfAttempts = updateRecords(user, questionIdHash,
                                                                                              score,
                                                                                              tries)
        db.session.commit()
        db.session.flush()

    return loadCurrentQuestions("mcq")


def clearTable():
    if DEBUG:
        users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId != "")
        for user in users:
            db.session.delete(user)
            db.session.commit()
            db.session.flush()
        print("Table is cleared.")
    else:
        print("Table can only be cleared in debug mode.")
