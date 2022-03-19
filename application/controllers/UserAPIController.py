from application.controllers.UserQuestionHandlerController import create_mc_questions, create_tf_questions
from flask import request


def generate_mc_question_api():
    """
    this method generate the multiple choice types of questions and store in json format
    :rtype: question information stored in json format
    """
    context = request.args['context']
    number_options = request.args['numberOptions']

    question_id_hashes, questions, options, answers = create_mc_questions(context, number_options)

    json_data = {'questions': questions, 'options': options, 'answers': answers}
    return json_data


def generate_tf_question_api():
    """
    this method generate the true and false types of questions and store in json format
    :rtype: question information stored in json format
    """
    context = request.args['context']

    question_id_hashes, questions, options, answers = create_tf_questions(context)

    json_data = {'questions': questions, 'options': options, 'answers': answers}
    return json_data
