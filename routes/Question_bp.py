from flask import Blueprint
from controllers.QuestionController import index, store, show, update, delete

Question_bp = Blueprint('Question_bp', __name__)

Question_bp.route('/', methods=['GET'])(index)
Question_bp.route('/create', methods=['POST'])(store)
Question_bp.route('/<int:user_id>', methods=['GET'])(show)
Question_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
Question_bp.route('/<int:user_id>', methods=['DELETE'])(delete)
