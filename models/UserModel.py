from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


class User(db.Model):
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
