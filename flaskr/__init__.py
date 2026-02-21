import os
from flask import Flask, render_template
from flask_login import current_user, LoginManager
from .group import group_bp
from .sch import sch_bp
from .user import User, user_bp
from .util import api_bp, bcrypt, db

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

bcrypt.init_app(app)
db.init_app(app)
with app.app_context():
    db.create_all()
login_manager = LoginManager(app)
login_manager.login_view = "user_bp.login"

app.register_blueprint(api_bp)
app.register_blueprint(group_bp)
app.register_blueprint(sch_bp)
app.register_blueprint(user_bp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index-login.html")
    return render_template("index.html")
