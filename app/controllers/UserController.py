import sys
from flask import render_template, redirect, url_for, request, abort
from models.User import User
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def index():
    return render_template('index.html')


def store():
    print("vannakam")
    email = request.form['email']
    password = request.form['password']
    print(email, password)
    return render_template('enterText.html')  # todo change this to user landing page


def show(userId):
    pass


def update(userId):
    pass


def delete(userId):
    pass
