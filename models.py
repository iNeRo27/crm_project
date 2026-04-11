from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#  User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  # make it unique
    password = db.Column(db.String(200))
    role = db.Column(db.String(10), default="user")  # user or admin

    requests = db.relationship('Request', backref='user', lazy=True)

#  Request Table
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(50))  # maintenance or consultation
    description = db.Column(db.Text)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default="Pending")