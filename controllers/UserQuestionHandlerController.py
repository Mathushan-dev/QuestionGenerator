import bcrypt
import random
from functions.distractorGenerator import generateChoices
from functions.falsifyStatement import falsifyStatement
from functions.keywordGenerator import findRandomKeyword
from functions.T5QuestionGenerator import applyT5Model
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from config import DEBUG

db = SQLAlchemy()


def generateTFQuestions():
    if DEBUG:
        print("generateTFQuestions called")
    context = request.form.get("context")  # todo assuming context is at least 5 words
    statements = context.split(".")
    if len(statements) == 0:
        return render_template('enterText.html')  # this should never occur as frontend validates input text is at
        # least 5 words

    questions = []
    answers = []
    for statement in statements:
        if random.choice([True, False]):
            questions.append(falsifyStatement(statement))
            answers.append(False)
        else:
            questions.append(statement)
            answers.append(True)
    # todo temporarily save answers somewhere with a unique id to use for marking
    render_template('trueFalse.html', questions=questions)


def generateMCQuestions():
    if DEBUG:
        print("generateMCQuestions called")
    context = request.form.get("context")  # todo assuming context is at least 5 words
    numberOptions = request.form.get("numberOptions")
    statements = context.split(".")
    if len(statements) == 0:
        return render_template('enterText.html')  # this should never occur as frontend validates input text is at
        # least 5 words

    questions = []
    options = []
    answers = []

    try:
        intNumberOptions = int(numberOptions)
    except ValueError:
        intNumberOptions = 4

    for statement in statements:
        answer = findRandomKeyword(statement)
        for question in applyT5Model(statement, findRandomKeyword(statement)):
            answers.append(answer)
            distractors = generateChoices(answer, intNumberOptions)
            options.append(distractors)
            questions.append(question)

    # todo temporarily save answers somewhere with a unique id to use for marking
    render_template('multipleChoice.html', questions=questions, options=options)
