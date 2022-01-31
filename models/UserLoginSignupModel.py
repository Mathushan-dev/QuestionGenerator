import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserLoginSignup(db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.String, primary_key=True)
    hashedPassword = db.Column(db.String)

    def __init__(self, userId, hashedPassword):
        self.userId = userId
        self.hashedPassword = hashedPassword

    @property
    def serialize(self):
        return {
            'userId': self.userId,
            'hashedPassword': self.hashedPassword
        }

    @staticmethod
    def makePasswordHash(password):
        hash = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())
        return hash.decode('utf-8')

    def isPasswordValid(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.hashedPassword.encode('utf-8'))
