from audioop import mul
from webbrowser import get
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


@bp.route("/my-courses")
@login_required
def my_courses():
    
    return render_template('views/my_courses.html', courses=courses)


@bp.route("/add-course", methods=['GET', 'POST'])
@login_required
def add_course():
    if request.method == "POST":
        multiselect = request.form.getlist('students')
        worker = session['user_id']
        name = request.form['title']
        description = request.form['description']

        course_id = insert_course(name, description)
        add_students_to_course(course_id, multiselect)
        add_worker_to_course(course_id, worker)
        flash('Pomyślnie dodano kurs i jego uczestników!')
        return redirect(url_for("views.index"))

    worker_faculty = get_user_faculty(session['user_id'])
    students = get_all_students_from_faculty(worker_faculty)
    return render_template('views/add_course.html', students=students)
