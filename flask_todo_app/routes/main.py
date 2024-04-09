from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required, logout_user

from .. import db
from ..models import Note, User

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
@login_required
def index():
    notes = Note.query.filter_by(user_id=current_user.id).all()

    return render_template("index.html", notes=notes)


@main.route("/notes/new", methods=["GET", "POST"])
@login_required
def notes_new():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        note = Note(title=title, description=description, user_id=current_user.id)

        db.session.add(note)
        db.session.commit()

        flash("Note successfully added.", category="success")
        return redirect(url_for("main.index"))

    return render_template(
        "note.html", title="New note", date="", note_title="", note_description=""
    )


@main.route("/notes/<int:id>", methods=["GET", "POST"])
@login_required
def notes_id(id):
    note = Note.query.get(id)

    if note.user_id != current_user.id:
        abort(404)

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        note.title = title
        note.description = description

        db.session.commit()

        flash("Note successfully updated.", category="success")
        return redirect(url_for("main.index"))

    return render_template(
        "note.html",
        title="Edit note",
        date=f"Updated on {note.updated_at.strftime('%I:%M %p, %A, %d %b, %Y')}",
        note_title=note.title,
        note_description=note.description,
    )


@main.route("/notes/<int:id>/delete", methods=["GET"])
@login_required
def notes_delete(id):
    Note.query.filter_by(id=id).delete()
    db.session.commit()

    flash("Note successfully deleted.", category="success")
    return redirect(url_for("main.index"))


@main.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":
        password = request.form["password"]
        password_new = request.form["password_new"]
        password_confirm = request.form["password_confirm"]

        if not current_user.check_password(password):
            flash(
                "Current password does not match. Try typing your password again.",
                category="error",
            )
            return redirect(url_for("main.account"))

        new_user = User()
        new_user.set_password(password_new)

        if not new_user.check_password(password_confirm):
            flash(
                "New password does not match. Try typing your password again.",
                category="error",
            )
            return redirect(url_for("main.account"))

        current_user.set_password(password_new)
        db.session.commit()

        flash("Password successfully changed.", category="success")
        return redirect(url_for("main.account"))

    return render_template("account.html")


@main.route("/account/delete", methods=["GET"])
@login_required
def account_delete():
    db.session.delete(current_user)
    db.session.commit()

    logout_user()

    flash("User successfully deleted.", category="success")
    return redirect(url_for("auth.login"))
