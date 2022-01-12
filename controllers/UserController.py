import bcrypt
from flask import render_template, request
from models.UserModel import User
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from config import DEBUG

db = SQLAlchemy()


def index():
    return render_template('index.html')


def store():
    userId = request.form['email']  # todo assuming email is valid in the frontend
    password = request.form['password']  # todo assuming passwordHash is strong in the frontend

    hashedPassword = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
    # if bcrypt.checkpw(passwordHash, hashedPassword) then matches

    user = User(userId, hashedPassword)
    try:
        db.session.add(user)
        db.session.flush()
    except IntegrityError:
        print("Email already exists. Error!!!")
        db.session.rollback()  # todo error page as user already exits
    finally:
        db.session.commit()
        return render_template('enterText.html')  # todo change this to user profile page


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
        print("Table is cleared.")
    else:
        print("Table can only be cleared in debug mode.")
