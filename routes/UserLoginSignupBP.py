from flask import Blueprint
from controllers.UserLoginSignupController import index, loginSignupForm, loadEnterText, signUp, logIn, logOut, loadHome, updatePassword, deleteAccount, saveQuestionAttributes

UserLoginSignupBP = Blueprint('UserLoginSignupBP', __name__)

UserLoginSignupBP.route('/', methods=['GET'])(index)
UserLoginSignupBP.route('/loginForm', methods=['POST', 'GET'])(loginSignupForm)
UserLoginSignupBP.route('/enterText', methods=['POST', 'GET'])(loadEnterText)
UserLoginSignupBP.route('/signUp', methods=['POST', 'GET'])(signUp)
UserLoginSignupBP.route('/logIn', methods=['POST', 'GET'])(logIn)
UserLoginSignupBP.route('/logOut', methods=['POST', 'GET'])(logOut)
UserLoginSignupBP.route('/loadHome', methods=['POST', 'GET'])(loadHome)
UserLoginSignupBP.route('/updatePassword', methods=['POST', 'GET'])(updatePassword)
UserLoginSignupBP.route('/deleteAccount', methods=['POST', 'GET'])(deleteAccount)
UserLoginSignupBP.route('/saveQuestionAttributes', methods=['POST', 'GET'])(saveQuestionAttributes)
