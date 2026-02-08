from datetime import date
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from .util import db, Group, Schedule

sch_bp = Blueprint("sch_bp", __name__)


@sch_bp.route("/add/<int:group_no>", methods=["GET", "POST"])
@login_required
def add(group_no: int):
    if request.method == "POST":
        user_id = current_user.id
        if not user_id:
            flash("사용자를 찾을 수 없습니다.")
            return redirect(url_for("index"))

        name = request.form.get("name")
        desc = request.form.get("desc")
        start = request.form.get("start")
        if start:
            start = date.fromisoformat(start)
        else:
            flash("날짜를 입력하지 않았습니다.")
            return redirect(url_for("sch_bp.add", group_no=group_no))
        end = request.form.get("end")
        if end:
            end = date.fromisoformat(end)
        else:
            flash("날짜를 입력하지 않았습니다.")
            return redirect(url_for("sch_bp.add", group_no=group_no))
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
    return render_template("add.html", group=group.name)  # type: ignore
