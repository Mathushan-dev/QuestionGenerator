import random
from functions.distractorGenerator import generateChoices
from functions.falsifyStatement import falsifyStatement
from functions.keywordGenerator import findRandomKeyword
from functions.T5QuestionGenerator import applyT5Model
from models.UserQuestionHandlerModel import UserQuestionHandler
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from config import DEBUG

db = SQLAlchemy()
firstLaunch = True


def addQuestionToDatabase(questionId, context, question, answer, options):
    global firstLaunch
    if firstLaunch:
        clearTable()
        firstLaunch = False

    optionsLinear = ""
    for option in options:
        optionsLinear += option
        optionsLinear += "}"

    question = UserQuestionHandler(questionId, context, question, answer, optionsLinear.strip())

    db.session.add(question)
    db.session.flush()
    db.session.commit()


def generateTFQuestions():
    if DEBUG:
        print("generateTFQuestions called")
    context = request.form.get("context")  # todo assuming context is at least 5 words
    statements = context.split(".")
    if len(statements) == 0:
        return render_template(
            'try-input-passage.html')  # this should never occur as frontend validates input text is at
        # least 5 words

    questionIdHashes = []
    questions = []
    options = []
    answers = []

    for statement in statements:
        if random.choice([True, False]):  # if a statement should be falsified
            questions.append(falsifyStatement(statement))
            answers.append(False)
        else:
            questions.append(statement)
            answers.append(True)

        options.append([True, False])
        questionIdHashes.append(
            UserQuestionHandler.makeQuestionIdHash(statement + questions[-1] + answers[-1] + ''.join(options[-1])))
        addQuestionToDatabase(questionIdHashes[-1], statement, questions[-1], answers[-1], options[-1])

    render_template('true-false-template.html', questionIdHashes=questionIdHashes, questions=questions, options=options,
                    answers=answers)


def generateMCQuestions():
    if DEBUG:
        print("generateMCQuestions called")
    context = request.form.get("context")  # todo assuming context is at least 5 words
    numberOptions = request.form.get("numberOptions")
    statements = context.split(".")
    if len(statements) == 0:
        return render_template(
            'try-input-passage.html')  # this should never occur as frontend validates input text is at
        # least 5 words

    questionIdHashes = []
    questions = []
    options = []
    answers = []

    try:
        intNumberOptions = int(numberOptions)
    except ValueError:
        intNumberOptions = 4
    finally:
        for statement in statements:
            if statement.strip() == "":
                continue
            answer = findRandomKeyword(statement)
            question = applyT5Model(statement, findRandomKeyword(statement))
            answers.append(answer.lower())
            distractors = generateChoices(answer, intNumberOptions)
            options.append(distractors)
            questions.append(question)

            questionIdHashes.append(
                UserQuestionHandler.makeQuestionIdHash(statement + questions[-1] + answers[-1] + ''.join(options[-1])))
            addQuestionToDatabase(questionIdHashes[-1], statement, questions[-1], answers[-1], options[-1])

        return render_template('multiple-choice-template.html', questionIdHashes=questionIdHashes, questions=questions,
                               options=options, answers=answers)


def clearTable():
    if DEBUG:
        questions = db.session.query(UserQuestionHandler).filter(UserQuestionHandler.questionId != "")
        for question in questions:
            db.session.delete(question)
            db.session.commit()
        print("Table is cleared.")
    else:
        print("Table can only be cleared in debug mode.")
