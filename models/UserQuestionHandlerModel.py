import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserQuestionHandler(db.Model):
    __tablename__ = 'questions'
    questionId = db.Column(db.String, primary_key=True)
    context = db.Column(db.String)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    options = db.Column(db.String)

    def __init__(self, questionId, context, question, answer, options):
        self.questionId = questionId
        self.context = context
        self.question = question
        self.answer = answer
        self.options = options

    @property
    def serialize(self):
        return {
            'questionId': self.questionId,
            'context': self.context,
            'question': self.question,
            'answer': self.answer,
            'options': self.options
        }

    @staticmethod
    def makeQuestionIdHash(questionId): # questionId = question
        hash = bcrypt.hashpw(password=questionId.encode('utf-8'), salt=bcrypt.gensalt())
        return hash.decode('utf-8')

    def isQuestionIdMatch(self, questionId):
        return bcrypt.checkpw(questionId.encode('utf-8'), self.questionId.encode('utf-8'))
