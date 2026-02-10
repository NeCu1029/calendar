from flask import abort, Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .util import db, Group, groups_sch, make_code, users_group, users_sch, Whitelist

group_bp = Blueprint("group_bp", __name__)


@group_bp.route("/group/<int:group_no>")
@login_required
def group(group_no: int):
    whitelist = Whitelist.query.filter_by(group=group_no, user=current_user.id).first()
    if not whitelist:
        abort(403)
    g = Group.query.filter_by(group_id=group_no).first()
    return render_template(
        "group/group.html",
        no=g.group_id,
        name=g.name,
        desc=g.desc,
        invite_code=g.invite_code,
        schs=groups_sch(g.group_id),
    )


@group_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        user_id = current_user.id
        if not user_id:
            flash("사용자를 찾을 수 없습니다.")
            return redirect(url_for("index"))
        name = request.form.get("name")
        desc = request.form.get("desc")
        code = make_code(10)

        group = Group(name=name, desc=desc, invite_code=code)
        db.session.add(group)
        db.session.flush()
        whitelist = Whitelist(group=group.group_id, user=user_id)
        db.session.add(whitelist)

        db.session.commit()
        flash("그룹이 생성되었습니다.")
        return redirect(url_for("group_bp.group", group_no=group.group_id))
    return render_template("group/create.html")


@group_bp.route("/join", methods=["GET", "POST"])
@login_required
def join():
    if request.method == "POST":
        user_id = current_user.id
        if not user_id:
            flash("사용자를 찾을 수 없습니다.")
            return redirect(url_for("index"))
        code = request.form.get("code")

        group = Group.query.filter_by(invite_code=code).first()
        if not group:
            flash("그룹을 찾을 수 없습니다.")
            return redirect(url_for("group_bp.join"))

        whitelist = Whitelist(group=group.group_id, user=user_id)
        db.session.add(whitelist)
        db.session.commit()
        flash("그룹에 가입했습니다.")
        return redirect(url_for("group_bp.group", group_no=group.group_id))
    return render_template("group/join.html")


@group_bp.route("/my")
@login_required
def my():
    return render_template(
        "group/my.html",
        groups=users_group(current_user.id),
        schs=users_sch(current_user.id),
    )
