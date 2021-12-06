import sys
from flask import render_template, redirect, url_for, request, abort
from models.QuestionModel import Question
from flask_sqlalchemy import SQLAlchemy
from controllers.keywordGenerator import findQuestionKeywords
from controllers.questionMatcher import findRelevantQuestions

db = SQLAlchemy()


def index():
    return render_template('index.html')


def store():
    text = request.form['hello']

    questionKeywords = findQuestionKeywords(text)
    relevantQuestionsId = findRelevantQuestions(text)

    # todo go through relevantQuestionIds and display the question to user in order of most matching
    # todo keywords to the least

    # todo this is how to save to the database
    # question = Question(1, "b", 2, "d", "e", "f")
    # db.session.add(question)
    # db.session.commit()

    # todo this is how to do a fetch query in python
    # studentResult = db.session.query(Student).filter(Student.id == 1)
    # for result in studentResult:
    #     print(result.fname)

    return render_template('success.html', data=questionKeywords)


def show(userId):
    pass


def update(userId):
    pass


def delete(userId):
    pass
