import os
from flask import Flask, render_template
from flask_login import LoginManager
from .user import bcrypt, db, User, user_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

bcrypt.init_app(app)
db.init_app(app)
with app.app_context():
    db.create_all()
login_manager = LoginManager(app)
login_manager.login_view = "user_bp.login"  # type: ignore

app.register_blueprint(user_bp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/group/<int:group_no>")
def group(group_no: int):
    return render_template("group.html", no=group_no)
