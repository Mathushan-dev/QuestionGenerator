from flask import Blueprint
from application.controllers.UserLoginSignupController import index, login_signup_form, load_enter_text, sign_up, log_in, log_out, load_home, delete_account, save_question_attributes

UserLoginSignupBP = Blueprint('UserLoginSignupBP', __name__)

UserLoginSignupBP.route('/', methods=['GET'])(index)
UserLoginSignupBP.route('/loginForm', methods=['POST', 'GET'])(login_signup_form)
UserLoginSignupBP.route('/enterText', methods=['POST', 'GET'])(load_enter_text)
UserLoginSignupBP.route('/signUp', methods=['POST', 'GET'])(sign_up)
UserLoginSignupBP.route('/logIn', methods=['POST', 'GET'])(log_in)
UserLoginSignupBP.route('/logOut', methods=['POST', 'GET'])(log_out)
UserLoginSignupBP.route('/loadHome', methods=['POST', 'GET'])(load_home)
UserLoginSignupBP.route('/deleteAccount', methods=['POST', 'GET'])(delete_account)
UserLoginSignupBP.route('/saveQuestionAttributes', methods=['POST', 'GET'])(save_question_attributes)
