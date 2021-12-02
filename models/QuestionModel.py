from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/qgen'
db = SQLAlchemy(app)


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    type = db.Column(db.String(120))  # Multiple choice? fill in the blank? etc.
    options = db.Column(db.String(120))  # optionA,optionB,optionC
    answer = db.Column(db.String(120))
    keywords = db.Columnn(db.String(120))  # keyword1,keyword2,keyword3

    def __init__(self, id, question, type, options, answer, keywords):
        self.id = id
        self.question = question
        self.type = type
        self.options = options
        self.answer = answer
        self.keywords = keywords

    @property
    def serialize(self):
        return {
            'id': self.id,
            'question': self.question,
            'type': self.type,
            'options': self.options,
            'answer': self.answer,
            'keywords': self.keywords
        }
