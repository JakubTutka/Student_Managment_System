from app.auth import login_required
from flask import (
Blueprint, redirect, render_template, request, url_for
)

from .auth import login_required


bp = Blueprint("views", __name__)

@bp.route("/")
def index():
    return render_template('views/index.html')

@bp.route("/add-course")
@login_required
def add_course():
    return render_template('views/add_course.html')