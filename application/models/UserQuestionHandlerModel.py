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
        todo
        :param question_id:
        :param context:
        :param question:
        :param answer:
        :param options:
        :param question_number:
        :param question_set_code:
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
        todo
        :return: Dict[str, Any]
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
        todo
        :param question_id:
        :return: str
        """
        hash_password = bcrypt.hashpw(password=question_id.encode('utf-8'), salt=bcrypt.gensalt())
        return hash_password.decode('utf-8')

    def is_question_id_match(self, question_id):
        """
        todo
        :param question_id:
        :return: bool
        """
        return bcrypt.checkpw(question_id.encode('utf-8'), self.questionId.encode('utf-8'))
