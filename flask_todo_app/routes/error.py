from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException

from .. import db

error = Blueprint("error", __name__)


@error.app_errorhandler(HTTPException)
def not_found(e):
    return render_template(
        "error.html",
        code=e.code,
        name=e.name,
        description=e.description,
    )
