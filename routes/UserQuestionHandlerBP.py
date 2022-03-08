from flask import Blueprint
from controllers.UserQuestionHandlerController import generateTFQuestions, generateMCQuestions, generateExistQuestions
from controllers.UserAPIController import generateMCQuestionAPI, generateTFQuestionAPI

UserQuestionHandlerBP = Blueprint('UserQuestionHandlerBP', __name__)

UserQuestionHandlerBP.route('/generateTFQuestions', methods=['POST', 'GET'])(generateTFQuestions)
UserQuestionHandlerBP.route('/generateMCQuestions', methods=['POST', 'GET'])(generateMCQuestions)
UserQuestionHandlerBP.route('/generateExistQuestions', methods=['POST', 'GET'])(generateExistQuestions)
UserQuestionHandlerBP.route('/generateMCQuestionAPI', methods=['POST', 'GET'])(generateMCQuestionAPI)
UserQuestionHandlerBP.route('/generateTFQuestionAPI', methods=['POST', 'GET'])(generateTFQuestionAPI)