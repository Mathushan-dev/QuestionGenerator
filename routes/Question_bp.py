from flask import render_template, request
from models.QuestionModel import app, Question, db
from flask import Blueprint
from controllers.QuestionController import index, store, show, update, destroy

Question_bp = Blueprint('Question_bp', __name__)
Question_bp.route('/', methods=['GET'])(index)
Question_bp.route('/create', methods=['POST'])(store)
Question_bp.route('/<int:user_id>', methods=['GET'])(show)
Question_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
Question_bp.route('/<int:user_id>', methods=['DELETE'])(destroy)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']

    question = Question(fname, lname, pet)
    db.session.add(question)
    db.session.commit()

    # this is how to do a fetch query in python
    # studentResult = db.session.query(Student).filter(Student.id == 1)
    # for result in studentResult:
    #     print(result.fname)

    return render_template('success.html', data=fname)
