from flask import Blueprint
from controllers.UserController import index, loginForm, signUp, logIn, show, update, delete

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/', methods=['GET'])(index)
user_bp.route('/loginForm', methods=['POST', 'GET'])(loginForm)
user_bp.route('/signUp', methods=['POST', 'GET'])(signUp)
user_bp.route('/logIn', methods=['POST', 'GET'])(logIn)
user_bp.route('/<int:user_id>', methods=['GET'])(show)
user_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
user_bp.route('/<int:user_id>', methods=['DELETE'])(delete)
