import random
from functions.distractorGenerator import generateChoices
from functions.falsifyStatement import falsifyStatement
from functions.keywordGenerator import findRandomKeyword
from functions.T5QuestionGenerator import applyT5Model
from models.UserQuestionHandlerModel import UserQuestionHandler
from models.UserLoginSignupModel import db
from flask import render_template, request
from config import DEBUG

firstLaunch = True

currentQuestionIdHashes = None
currentQuestions = None
currentOptions = None
currentAnswers = None


def addQuestionToDatabase(questionId, context, question, answer, options):
    global firstLaunch
    if firstLaunch:
        clearTable()
        firstLaunch = False

    optionsLinear = ""
    for i in range(0, len(options)):
        option = str(options[i])
        optionsLinear += option
        if i == len(options) - 1:
            break
        optionsLinear += ","

    question = UserQuestionHandler(questionId.strip(), context.strip(), question.strip(), str(answer).strip(),
                                   optionsLinear.strip())

    db.session.add(question)
    db.session.commit()


def saveCurrentQuestions(questionIdHashes, questions, options, answers):
    global currentQuestionIdHashes, currentQuestions, currentOptions, currentAnswers

    currentQuestionIdHashes = questionIdHashes
    currentQuestions = questions
    currentOptions = options
    currentAnswers = answers


def loadCurrentQuestions(choice):
    # Structured in this way to allow for different templates for different types of questions during project extension
    if choice == "mcq":
        return render_template('multiple-choice-template.html', questionIdHashes=currentQuestionIdHashes,
                               questions=currentQuestions, options=currentOptions, answers=currentAnswers)
    return render_template('multiple-choice-template.html', questionIdHashes=currentQuestionIdHashes,
                           questions=currentQuestions, options=currentOptions, answers=currentAnswers)


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
        if statement.strip() == "":
            continue
        if random.choice([True, False]):  # if a statement should be falsified
            questions.append(falsifyStatement(statement))
            answers.append("False")
        else:
            questions.append(statement)
            answers.append("True")

        options.append(["True", "False"])
        questionIdHashes.append(
            UserQuestionHandler.makeQuestionIdHash(statement + questions[-1] + answers[-1] + ''.join(options[-1])))
        addQuestionToDatabase(questionIdHashes[-1], statement, questions[-1], answers[-1], options[-1])

    saveCurrentQuestions(questionIdHashes, questions, options, answers)
    return loadCurrentQuestions("tf")


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

        saveCurrentQuestions(questionIdHashes, questions, options, answers)
        return loadCurrentQuestions("mcq")


def clearTable():
    if DEBUG:
        questions = db.session.query(UserQuestionHandler).filter(UserQuestionHandler.questionId != "")
        for question in questions:
            db.session.delete(question)
            db.session.commit()
        print("Table is cleared.")
    else:
        print("Table can only be cleared in debug mode.")
