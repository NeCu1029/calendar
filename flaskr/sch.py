from flask import Blueprint, render_template
from flask_login import login_required
from .util import db, Group, Schedule

sch_bp = Blueprint("sch_bp", __name__)


@sch_bp.route("/add/<int:group_no>")
@login_required
def add(group_no: int):
    group = Group.query.filter_by(group_id=group_no).first()
    return render_template("add.html", group=group.name)  # type: ignore
