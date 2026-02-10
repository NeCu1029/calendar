from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, login_required, logout_user
from .util import bcrypt, db, User

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()

        if not user:
            flash("아이디가 존재하지 않습니다.")
        elif not bcrypt.check_password_hash(
            user.password, request.form.get("password")
        ):
            flash("비밀번호가 일치하지 않습니다.")
        else:
            login_user(user)
            return redirect(url_for("index"))
    return render_template("auth/login.html")


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = bcrypt.generate_password_hash(request.form.get("password")).decode(
            "utf-8"
        )
        email = request.form.get("email")

        if not User.query.filter_by(username=request.form.get("username")).first():
            user = User(username=username, password=password, email=email)
            db.session.add(user)
            db.session.commit()
            flash("정상적으로 회원가입 되었습니다.")
            return redirect(url_for("user_bp.login"))
        flash("이미 존재하는 아이디입니다.")
    return render_template("auth/register.html")


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("정상적으로 로그아웃 되었습니다.")
    return redirect(url_for("index"))
