import random
from functions.DistractorGenerator import generate_choices
from functions.StatementFalsifier import falsify_statement
from functions.KeywordFinder import find_random_keyword
from functions.T5QuestionGenerator import apply_t5_model
from models.UserQuestionHandlerModel import UserQuestionHandler
from models.UserLoginSignupModel import db
from flask import render_template, request
from config import DEBUG

firstLaunch = True

currentQuestionIdHashes = None
currentQuestions = None
currentOptions = None
currentAnswers = None
currentContext = None


def add_question_to_database(question_id, context, question, answer, options, question_number, question_set_code):
    """
    todo
    :param question_id:
    :param context:
    :param question:
    :param answer:
    :param options:
    :param question_number:
    :param question_set_code:
    :return: None
    """
    global firstLaunch
    if firstLaunch:
        clear_table()
        firstLaunch = False

    options_linear = ""
    for i in range(0, len(options)):
        option = str(options[i])
        options_linear += option
        if i == len(options) - 1:
            break
        options_linear += ","

    question = UserQuestionHandler(question_id.strip(), context.strip(), question.strip(), str(answer).strip(),
                                   options_linear.strip(), str(question_number).strip(), question_set_code.strip())

    db.session.add(question)
    db.session.commit()


def save_current_questions(question_id_hashes, questions, options, answers, context):
    """
    todo
    :param question_id_hashes:
    :param questions:
    :param options:
    :param answers:
    :param context:
    :return: None
    """
    global currentQuestionIdHashes, currentQuestions, currentOptions, currentAnswers

    currentQuestionIdHashes = question_id_hashes
    currentQuestions = questions
    currentOptions = options
    currentAnswers = answers
    currentContext = context


def load_current_questions(choice):
    """
    todo
    :param choice:
    :return: str
    """
    # Structured in this way to allow for different templates for different types of questions during project extension
    if choice == "mcq":
        return render_template('multiple-choice-template.html', questionIdHashes=currentQuestionIdHashes,
                               questions=currentQuestions, options=currentOptions, answers=currentAnswers,
                               context=currentContext)
    return render_template('multiple-choice-template.html', questionIdHashes=currentQuestionIdHashes,
                           questions=currentQuestions, options=currentOptions, answers=currentAnswers,
                           context=currentContext)


def generate_tf_questions():
    """
    todo
    :return: str
    """
    if DEBUG:
        print("generateTFQuestions called")
    context = request.form.get("context")

    if len(context.split(".")) == 0:
        return render_template(
            'try-input-passage.html')  # this should never occur as frontend validates input text is at
        # least 5 words

    question_id_hashes, questions, options, answers = create_tf_questions(context)
    save_current_questions(question_id_hashes, questions, options, answers, context)

    return load_current_questions("tf")


def create_tf_questions(context):
    """
    todo
    :param context:
    :return: Tuple[List[str], List[str], List[List[str]], List[str]]
    """
    statements = context.split(".")

    question_id_hashes = []
    questions = []
    options = []
    answers = []

    question_number = 0
    question_set_code = UserQuestionHandler.make_question_id_hash(context)
    for statement in statements:
        if statement.strip() == "":
            continue
        question_number += 1
        if random.choice([True, False]):  # if a statement should be falsified
            questions.append(falsify_statement(statement))
            answers.append("False")
        else:
            questions.append(statement)
            answers.append("True")

        options.append(["True", "False"])
        question_id_hashes.append(
            UserQuestionHandler.make_question_id_hash(statement + questions[-1] + answers[-1] + ''.join(options[-1])))
        add_question_to_database(question_id_hashes[-1], statement, questions[-1], answers[-1], options[-1],
                                 question_number,
                                 question_set_code)

    return question_id_hashes, questions, options, answers


def generate_mc_questions():
    """
    todo
    :return: str
    """
    if DEBUG:
        print("generateMCQuestions called")
    context = request.form.get("context")
    number_options = request.form.get("numberOptions")

    if len(context.split(".")) == 0:
        return render_template(
            'try-input-passage.html')  # this should never occur as frontend validates input text is at
        # least 5 words

    question_id_hashes, questions, options, answers = create_mc_questions(context, number_options)
    save_current_questions(question_id_hashes, questions, options, answers, context)

    return load_current_questions("mcq")


def create_mc_questions(context, number_options):
    """
    todo
    :param context:
    :param number_options:
    :return: Tuple[List[str], list, List[list], list]
    """
    statements = context.split(".")

    question_id_hashes = []
    questions = []
    options = []
    answers = []

    try:
        int_number_options = int(number_options)
    except ValueError:
        int_number_options = 4
    finally:
        question_number = 0
        question_set_code = UserQuestionHandler.make_question_id_hash(context)
        for statement in statements:
            if statement.strip() == "":
                continue
            question_number += 1
            answer = find_random_keyword(statement)
            question = apply_t5_model(statement, find_random_keyword(statement))
            answers.append(answer.lower())
            distractors = generate_choices(answer, int_number_options)
            options.append(distractors)
            questions.append(question)

            question_id_hashes.append(
                UserQuestionHandler.make_question_id_hash(
                    statement + questions[-1] + answers[-1] + ''.join(options[-1])))
            add_question_to_database(question_id_hashes[-1], statement, questions[-1], answers[-1], options[-1],
                                     question_number, question_set_code)

        return question_id_hashes, questions, options, answers


def generate_exist_questions():
    """
    todo
    :return: str
    """
    if DEBUG:
        print("generateExistQuestions called")
    question_set_code = request.form.get("context")

    if question_set_code.strip() == "":
        return render_template(
            'try-input-passage.html')  # this should never occur as frontend validates input text is at
        # least 5 words

    questions_all = db.session.query(UserQuestionHandler).filter(
        UserQuestionHandler.questionSetCode == question_set_code).all()
    db.session.flush()

    if len(questions_all) == 0:
        return render_template('try-input-passage.html')

    question_id_hashes = []
    questions = []
    options = []
    answers = []

    for question in questions_all:
        question_id_hashes.append(question.questionId)
        questions.append(question.question)
        options.append(question.options.split(","))
        answers.append(question.answer)

    save_current_questions(question_id_hashes, questions, options, answers, context)

    return load_current_questions("tf")


def clear_table():
    """
    todo
    :return: None
    """
    if DEBUG:
        questions = db.session.query(UserQuestionHandler).filter(UserQuestionHandler.questionId != "")
        for question in questions:
            db.session.delete(question)
            db.session.commit()
        print("Table is cleared.")
    else:
        print("Table can only be cleared in debug mode.")
