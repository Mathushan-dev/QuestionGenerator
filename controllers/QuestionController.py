import sys
from flask import render_template, redirect, url_for, request, abort
from models.QuestionModel import Question

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def index():
    return render_template('index.html')


def store():
    text = request.form['text']

    question = Question(fname, lname, pet)
    db.session.add(question)
    db.session.commit()

    # this is how to do a fetch query in python
    # studentResult = db.session.query(Student).filter(Student.id == 1)
    # for result in studentResult:
    #     print(result.fname)

    return render_template('success.html', data=fname)


def show(userId):
    pass


def update(userId):
    pass


def delete(userId):
    pass
