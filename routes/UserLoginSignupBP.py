from flask import Blueprint
from controllers.UserLoginSignupController import index, loginSignupForm, signUp, logIn, updatePassword, deleteAccount

UserLoginSignupBP = Blueprint('UserLoginSignupBP', __name__)

UserLoginSignupBP.route('/', methods=['GET'])(index)
UserLoginSignupBP.route('/loginForm', methods=['POST', 'GET'])(loginSignupForm)
UserLoginSignupBP.route('/signUp', methods=['POST', 'GET'])(signUp)
UserLoginSignupBP.route('/logIn', methods=['POST', 'GET'])(logIn)
UserLoginSignupBP.route('/updatePassword', methods=['POST', 'GET'])(updatePassword)
UserLoginSignupBP.route('/deleteAccount', methods=['POST', 'GET'])(deleteAccount)
