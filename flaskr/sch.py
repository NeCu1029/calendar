from datetime import date
from flask import abort, Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .util import db, Group, Schedule

sch_bp = Blueprint("sch_bp", __name__)


@sch_bp.route("/add/<int:group_no>", methods=["GET", "POST"])
@login_required
def add(group_no: int):
    user_id = current_user.id
    if not user_id:
        flash("사용자를 찾을 수 없습니다.")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("desc")
        start = date.fromisoformat(request.form.get("start"))
        end = date.fromisoformat(request.form.get("end"))
        if start > end:
            flash("종료일은 시작일 이전일 수 없습니다.")
            return redirect(url_for("sch_bp.add", group_no=group_no))

        sch = Schedule(
            creator=user_id, group=group_no, name=name, desc=desc, start=start, end=end
        )
        db.session.add(sch)
        db.session.commit()
        flash("일정이 생성되었습니다.")
        return redirect(url_for("group_bp.group", group_no=group_no))

    group = Group.query.filter_by(group_id=group_no).first()
    return render_template("sch/add.html", group=group.name)


@sch_bp.route("/modify/<int:sch_no>", methods=["GET", "POST"])
@login_required
def modify(sch_no: int):
    sch = Schedule.query.filter_by(no=sch_no).first()
    if not sch:
        abort(404)
    user_id = current_user.id
    if not user_id:
        flash("사용자를 찾을 수 없습니다.")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name")
        desc = request.form.get("desc")
        start = date.fromisoformat(request.form.get("start"))
        end = date.fromisoformat(request.form.get("end"))
        if start > end:
            flash("종료일은 시작일 이전일 수 없습니다.")
            return redirect(url_for("sch_bp.modify", sch_no=sch_no))

        sch.name = name
        sch.desc = desc
        sch.start = start
        sch.end = end
        db.session.commit()
        flash("일정이 수정되었습니다.")
        return redirect(url_for("group_bp.group", group_no=sch.group))
    return render_template(
        "sch/modify.html", name=sch.name, desc=sch.desc, start=sch.start, end=sch.end
    )
