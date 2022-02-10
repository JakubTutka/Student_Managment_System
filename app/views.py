from app.auth import login_required
from flask import (
    Blueprint, redirect, render_template, request, url_for, session, flash
)

from .auth import login_required
from .database import (
    mysql, get_all_students_from_faculty, get_user_faculty, insert_course, add_worker_to_course, add_students_to_course,
    get_user_name
)


bp = Blueprint("views", __name__)


@bp.route("/")
def index():
    user = None
    if session.get('user_id') is not None:
        user = get_user_name(session['user_id'])
    return render_template('views/index.html', user=user)

@bp.route("/map")
def map():
    return render_template("views/map.html")
