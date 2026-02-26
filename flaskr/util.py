# 잡다한 것들

import random
from datetime import timedelta
from flask import Blueprint, jsonify
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")
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

    def to_dict(self, user_id: int):
        return {
            "no": self.no,
            "creator": self.creator,
            "group": self.group,
            "title": self.name,
            "desc": self.desc,
            "start": self.start.isoformat(),
            "end": (self.end + timedelta(days=1)).isoformat(),
            "by_me": self.creator == user_id,
        }


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


@api_bp.route("/get_user_sch")
@login_required
def get_user_sch():
    user_id = current_user.id
    if not user_id:
        return jsonify([])
    groups = (
        db.session.query(Group)
        .join(Whitelist, Group.group_id == Whitelist.group)
        .filter(Whitelist.user == user_id)
        .all()
    )
    group_ids = [g.group_id for g in groups]
    res = Schedule.query.filter(Schedule.group.in_(group_ids)).all()
    return jsonify([sch.to_dict(user_id) for sch in res])


@api_bp.route("/get_group_sch/<int:group_no>")
@login_required
def get_group_sch(group_no: int):
    user_id = current_user.id
    res = Schedule.query.filter_by(group=group_no).all()
    return jsonify([sch.to_dict(user_id) for sch in res])
