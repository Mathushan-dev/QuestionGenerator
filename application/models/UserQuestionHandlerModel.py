import bcrypt
from application.models.UserLoginSignupModel import db


class UserQuestionHandler(db.Model):
    __tablename__ = 'questions'
    questionId = db.Column(db.String, primary_key=True)
    context = db.Column(db.String)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    options = db.Column(db.String)
    questionNumber = db.Column(db.String)
    questionSetCode = db.Column(db.String)

    def __init__(self, question_id, context, question, answer, options, question_number, question_set_code):
        """
        :param question_id: question id
        :param context: context to generate questions
        :param question: question text
        :param answer: answer of the question
        :param options: options to choose
        :param question_number: number of the question
        :param question_set_code: hash of the context
        """
        self.questionId = question_id
        self.context = context
        self.question = question
        self.answer = answer
        self.options = options
        self.questionNumber = question_number
        self.questionSetCode = question_set_code

    @property
    def serialize(self):
        """
        :return: data in dictionary
        """
        return {
            'questionId': self.questionId,
            'context': self.context,
            'question': self.question,
            'answer': self.answer,
            'options': self.options,
            'questionNumber': self.questionNumber,
            'questionSetCode': self.questionSetCode
        }

    @staticmethod
    def make_question_id_hash(question_id):  # questionId = question
        """
        :param question_id: question id
        :return: hashed question id
        """
        hash_password = bcrypt.hashpw(password=question_id.encode('utf-8'), salt=bcrypt.gensalt())
        return hash_password.decode('utf-8')

    def is_question_id_match(self, question_id):
        """
        :param question_id: question id
        :return: bool
        """
        return bcrypt.checkpw(question_id.encode('utf-8'), self.questionId.encode('utf-8'))
