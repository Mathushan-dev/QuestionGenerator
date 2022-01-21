import bcrypt
from flask import render_template, request
from models.UserModel import User
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from config import DEBUG

db = SQLAlchemy()


def index():
    clearTable()
    if DEBUG:
        print("index called")
    return render_template('index.html')


def loginForm(message=""):
    if DEBUG:
        print("loginForm called", message)
    return render_template('login.html', loginErrorMessage=message)


def signUp():
    if DEBUG:
        print("signUp called")
    userId = request.form.get("email")  # todo assuming email is valid in the frontend
    password = request.form.get("password")  # todo assuming passwordHash is strong in the frontend

    passwordHash = User.makePasswordHash(password)
    user = User(userId, passwordHash)

    try:
        db.session.add(user)
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return loginForm(message="Those records already exist on the server, please log in instead.")
    db.session.commit()
    return render_template('enterText.html')


def logIn():
    if DEBUG:
        print("logIn called")
    userId = request.form.get("email")  # todo assuming email is valid in the frontend
    password = request.form.get("password")  # todo assuming password is strong in the frontend

    users = db.session.query(User).filter(User.userId == userId).all()
    db.session.flush()
    if len(users) == 0:
        return loginForm(message="Those records do not exist on the server, please sign up instead.")
    elif len(users) != 1:
        return loginForm(message="The server is currently down. Please try logging in later.")
        # This should never happen and something has gone terribly wrong if duplicate emails exist on database
    else:
        if users[0].isPasswordValid(password):
            return render_template('enterText.html')  # todo change to user homepage
        return loginForm(message="The password is incorrect.")


def show(userId):
    users = db.session.query(User).filter(User.userId == userId)
    print(users[0].userId, users[0].hashedPassword)
    # todo change this to user profile page
    # return render_template('')


def update(userId):
    pass


def delete(userId):
    users = db.session.query(User).filter(User.userId == userId)
    stackTrace = db.session.delete(users[0])
    print("The record for", userId, "has been deleted successfully.\n", stackTrace)


def clearTable():
    if DEBUG:
        users = db.session.query(User).filter(User.userId != "")
        for user in users:
            db.session.delete(user)
            db.session.commit()
        print("Table is cleared.")
    else:
        print("Table can only be cleared in debug mode.")
