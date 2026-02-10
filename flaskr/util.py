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


class Schedule(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.Integer, unique=False, nullable=False)
    group = db.Column(db.Integer, unique=False, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    desc = db.Column(db.String(500), unique=False, nullable=True)
    start = db.Column(db.Date, unique=False, nullable=False)
    end = db.Column(db.Date, unique=False, nullable=False)


def make_code(length: int) -> str:
    while True:
        lst = []
        for _ in range(length):
            lst.append(chr(random.randint(0, 25) + 97))
        res = "".join(lst)
        group = Group.query.filter_by(invite_code=res).first()
        if not group:
            return "".join(lst)


def users_group(user_id: int) -> list[int]:
    """Return A List Of Groups In Which A User Is Participated"""
    return (
        db.session.query(Group)
        .join(Whitelist, Group.group_id == Whitelist.group)
        .filter(Whitelist.user == user_id)
        .all()
    )


def users_sch(user_id: int) -> list[int]:
    """Return A List Of Schedules Which A User Created"""
    return Schedule.query.filter_by(creator=user_id).all()


def groups_sch(group_no: int) -> list[int]:
    """Return A List Of Schedules Which Belong to A Group"""
    return Schedule.query.filter_by(group=group_no).all()
