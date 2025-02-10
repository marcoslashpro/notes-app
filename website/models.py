from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False) 
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    notes = db.relationship('Note')

    def __repr__(self):
        return f'<User {self.username}>'


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_title = db.Column(db.String(10000), unique=False, nullable=False)
    note_content = db.Column(db.String(100000), unique=False, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Title {self.note_title}, Content {self.note_content}>'
