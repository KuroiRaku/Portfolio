from datetime import datetime
from sqlalchemy_utils import URLType
from wtforms.validators import Regexp
from flask_login import UserMixin
import __init__
from __init__ import db


class Project(db.Model):
    __bind_key__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(30),
                      unique=True,
                      nullable=False,
                      info={"validators": Regexp("^[A-Za-z0-9_-]*$")})
    imgfile = db.Column(db.String(30), nullable=False)
    website = db.Column(db.String(70), nullable=True)
    github_url = db.Column( db.String(70),nullable=False)
    is_game = db.Column(db.Boolean)
    description = db.Column(db.Text, nullable=False)
    long_desc = db.Column(db.Text, nullable=False)
    index = db.Column(db.Integer, autoincrement=True, nullable=False)


    def __repr__(self):
        return f"<Project title: {self.title}>"

class Test(db.Model):
    __bind_key__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User username: {self.username}>"
