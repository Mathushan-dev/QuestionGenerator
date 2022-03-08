import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserLoginSignup(db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.String, primary_key=True)
    fName = db.Column(db.String)
    lName = db.Column(db.String)
    hashedPassword = db.Column(db.String)
    attemptedQuestionIds = db.Column(db.String)  # id, id2, id3
    questionScores = db.Column(db.String)  # 1, 0, 1 - means id and id3 answered correctly but id2 answered incorrectly
    numberOfAttempts = db.Column(db.String)  # 4, 4, 1, 3 - means 4 tries till correct answer on first two questions
    # and then 1 and 3 tries in the following questions
    attemptedDates = db.Column(db.String)
    attemptedTimes = db.Column(db.String)

    def __init__(self, user_id, f_name, l_name, hashed_password):
        """
        todo
        :param user_id:
        :param f_name:
        :param l_name:
        :param hashed_password:
        """
        self.userId = user_id
        self.fName = f_name
        self.lName = l_name
        self.hashedPassword = hashed_password
        self.attemptedQuestionIds = ""
        self.questionScores = ""
        self.numberOfAttempts = ""
        self.attemptedDates = ""
        self.attemptedTimes = ""

    @property
    def serialize(self):
        """
        todo
        :return: Dict[str, str]
        """
        return {
            'userId': self.userId,
            'fName': self.fName,
            'lName': self.lName,
            'hashedPassword': self.hashedPassword,
            'attemptedQuestionIds': self.attemptedQuestionIds,
            'questionScores': self.questionScores,
            'numberOfAttempts': self.numberOfAttempts,
            'attemptedDates': self.attemptedDates,
            'attemptedTimes': self.attemptedTimes,
            'attemptedOrders': self.attemptedOrders
        }

    @staticmethod
    def make_password_hash(password):
        """
        todo
        :param password:
        :return: str
        """
        hash_password = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())
        return hash_password.decode('utf-8')

    def is_password_valid(self, password):
        """
        todo
        :param password:
        :return: bool
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.hashedPassword.encode('utf-8'))
