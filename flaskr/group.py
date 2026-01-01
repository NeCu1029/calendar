from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from .util import db

group_bp = Blueprint("group_bp", __name__)


class Group(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    desc = db.Column(db.String(500), unique=False, nullable=True)


@group_bp.route("/group/<int:group_no>")
@login_required
def group(group_no: int):
    return render_template("group/group.html", no=group_no)


@group_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("desc")

        group = Group(name=name, desc=desc)  # type: ignore
        db.session.add(group)
        db.session.commit()
        flash("그룹이 생성되었습니다.")
        return redirect(url_for("group_bp.group", group_no=group.group_id))
    return render_template("group/create.html")
