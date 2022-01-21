import bcrypt
from flask import render_template, request
from models.UserLoginSignupModel import UserLoginSignup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from config import DEBUG

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
    return render_template('index.html')


def loginSignupForm(message=""):
    if DEBUG:
        print("loginForm called", message)
    return render_template('login.html', loginErrorMessage=message)


def signUp():
    if DEBUG:
        print("signUp called")
    userId = request.form.get("email")  # todo assuming email is valid in the frontend
    password = request.form.get("password")  # todo assuming passwordHash is strong in the frontend

    passwordHash = UserLoginSignup.makePasswordHash(password)
    user = UserLoginSignup(userId, passwordHash)

    try:
        db.session.add(user)
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return loginSignupForm(message="Those records already exist on the server, please log in instead.")
    db.session.commit()
    global LoggedOnUserId
    LoggedOnUserId = userId
    return render_template('enterText.html')


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
            return render_template('enterText.html')  # todo change to user homepage
        return loginSignupForm(message="The password is incorrect.")


def loadHome():
    pass
    # todo change this to user profile page
    # return render_template('')


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
        except:
            print(stackTrace)
        return index()


def clearTable():
    if DEBUG:
        users = db.session.query(UserLoginSignup).filter(UserLoginSignup.userId != "")
        for user in users:
            db.session.delete(user)
            db.session.commit()
        print("Table is cleared.")
    else:
        print("Table can only be cleared in debug mode.")
