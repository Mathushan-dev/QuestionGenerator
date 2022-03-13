from flask import Blueprint
from controllers.UserQuestionHandlerController import generate_tf_questions, generate_mc_questions, \
    generate_exist_questions, load_current_questions
from controllers.UserAPIController import generate_mc_question_api, generate_tf_question_api

UserQuestionHandlerBP = Blueprint('UserQuestionHandlerBP', __name__)

UserQuestionHandlerBP.route('/generateTFQuestions', methods=['POST', 'GET'])(generate_tf_questions)
UserQuestionHandlerBP.route('/generateMCQuestions', methods=['POST', 'GET'])(generate_mc_questions)
UserQuestionHandlerBP.route('/generateExistQuestions', methods=['POST', 'GET'])(generate_exist_questions)
UserQuestionHandlerBP.route('/generateMCQuestionAPI', methods=['POST', 'GET'])(generate_mc_question_api)
UserQuestionHandlerBP.route('/generateTFQuestionAPI', methods=['POST', 'GET'])(generate_tf_question_api)
UserQuestionHandlerBP.route('/loadCurrentQuestions', methods=['POST', 'GET'])(load_current_questions)
