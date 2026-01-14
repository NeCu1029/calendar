from flask import abort, Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .util import db

group_bp = Blueprint("group_bp", __name__)


class Group(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    desc = db.Column(db.String(500), unique=False, nullable=True)


class Whitelist(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.Integer, unique=False, nullable=False)
    user = db.Column(db.Integer, unique=False, nullable=False)


@group_bp.route("/group/<int:group_no>")
@login_required
def group(group_no: int):
    whitelist = Whitelist.query.filter_by(group=group_no, user=current_user.id).first()
    if not whitelist:
        abort(403)
    g = Group.query.filter_by(group_id=group_no).first()
    return render_template("group/group.html", name=g.name, desc=g.desc)  # type: ignore


@group_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("desc")
        user_id = current_user.id
        if not user_id:
            flash("사용자를 찾을 수 없습니다.")
            return redirect(url_for("index"))

        group = Group(name=name, desc=desc)  # type: ignore
        db.session.add(group)
        db.session.flush()
        whitelist = Whitelist(group=group.group_id, user=user_id)  # type: ignore
        db.session.add(whitelist)

        db.session.commit()
        flash("그룹이 생성되었습니다.")
        return redirect(url_for("group_bp.group", group_no=group.group_id))
    return render_template("group/create.html")


@group_bp.route("/my")
@login_required
def my():
    groups = (
        db.session.query(Group)
        .join(Whitelist, Group.group_id == Whitelist.group)
        .filter(Whitelist.user == current_user.id)
        .all()
    )

    return render_template("group/my.html", groups=groups)
