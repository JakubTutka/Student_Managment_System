from flask import (
    Blueprint, render_template, request, url_for, session, flash, redirect
)

from .auth import login_required
from .database import *

bp = Blueprint("faculties", __name__)

@bp.route("/faculties")
def show_faculties():
    if session.get('user_id') is not None:
        user_faculty_id = get_user_faculty(session['user_id'])[0]
    else:
        user_faculty_id = None
    faculties = get_all_faculties()
    return render_template('faculties/faculties.html', user_fid=user_faculty_id, faculties=faculties)

@bp.route("/faculty/<int:id>")
@login_required
def show_faculty_info(id):
    workers = get_all_workers_from_faculty(id)
    buildings = get_all_faculty_buildings(id)
    return render_template('faculties/show_faculty_info.html', workers=workers, buildings=buildings, title=get_faculty_name)