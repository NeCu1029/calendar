# 잡다한 것들

import random
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)


class Group(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    desc = db.Column(db.String(500), unique=False, nullable=True)
    invite_code = db.Column(db.String(10), unique=True, nullable=False)


class Whitelist(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.Integer, unique=False, nullable=False)
    user = db.Column(db.Integer, unique=False, nullable=False)


def make_code(length: int) -> str:
    while True:
        lst = []
        for _ in range(length):
            lst.append(chr(random.randint(0, 25) + 97))
        res = "".join(lst)
        group = Group.query.filter_by(invite_code=res).first()
        if not group:
            return "".join(lst)
