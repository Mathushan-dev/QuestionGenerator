from controllers.UserQuestionHandlerController import createMCQuestions, createTFQuestions
from flask import request
import requests


def generateMCQuestionAPI():
    context = request.args['context']
    numberOptions = request.args['numberOptions']

    questionIdHashes, questions, options, answers = createMCQuestions(context, numberOptions)

    json_data = {'questions': questions, 'options': options, 'answers': answers}
    return requests.post(json=json_data)


def generateTFQuestionAPI():
    context = request.args['context']

    questionIdHashes, questions, options, answers = createTFQuestions(context)

    json_data = {'questions': questions, 'options': options, 'answers': answers}
    return requests.post(json=json_data)

# url='http://example.com/api/foobar', json=json_data
