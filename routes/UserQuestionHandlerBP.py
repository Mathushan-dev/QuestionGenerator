from flask import Blueprint
from controllers.UserQuestionHandlerController import generateTFQuestions, generateMCQuestions

UserQuestionHandlerBP = Blueprint('UserQuestionHandlerBP', __name__)

UserQuestionHandlerBP.route('/generateTFQuestions', methods=['POST', 'GET'])(generateTFQuestions)
UserQuestionHandlerBP.route('/generateMCQuestions', methods=['POST', 'GET'])(generateMCQuestions)

