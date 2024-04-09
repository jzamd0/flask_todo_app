from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .. import db
from ..models import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        found = User.query.filter_by(username=username).first()

        if not found or not found.check_password(password):
            flash(
                "Wrong username or password. Please check your username or password.",
                category="error",
            )
            return redirect(url_for("auth.login"))

        login_user(found)

        return redirect(url_for("main.index"))

    return render_template("login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["password_confirm"]

        user = User(username=username)
        user.set_password(password)

        found = User.query.filter_by(username=username).first()

        if found:
            flash("Username is already taken. Try another username.", category="error")
            return redirect(url_for("auth.signup"))

        if not user.check_password(confirm_password):
            flash(
                "Passwords does not match. Try typing your password again.",
                category="error",
            )
            return redirect(url_for("auth.signup"))

        db.session.add(user)
        db.session.commit()

        flash("User successfully created.", category="success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html")


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()

    flash("You have successfully logged out.", category="success")
    return redirect(url_for("auth.login"))
