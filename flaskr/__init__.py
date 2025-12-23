from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("auth/login.html")


@app.route("/register")
def register():
    return render_template("auth/register.html")


@app.route("/group/<int:group_no>")
def group(group_no: int):
    return render_template("group.html", no=group_no)
