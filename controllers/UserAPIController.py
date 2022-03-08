from controllers.UserQuestionHandlerController import create_mc_questions, create_tf_questions
from flask import request


def generate_mc_question_api():
    """
    todo
    :rtype: object
    """
    context = request.args['context']
    number_options = request.args['numberOptions']

    question_id_hashes, questions, options, answers = create_mc_questions(context, number_options)

    json_data = {'questions': questions, 'options': options, 'answers': answers}
    return json_data


def generate_tf_question_api():
    """
    todo
    :rtype: object
    """
    context = request.args['context']

    question_id_hashes, questions, options, answers = create_tf_questions(context)

    json_data = {'questions': questions, 'options': options, 'answers': answers}
    return json_data
