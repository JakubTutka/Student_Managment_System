from flask import (
    Blueprint, render_template, request, url_for, session, flash, redirect
)

from .auth import login_required
from .database import *

bp = Blueprint("courses", __name__)

@bp.route("/add-course", methods=['GET', 'POST'])
@login_required
def add_course():
    if request.method == "POST":
        multiselect = request.form.getlist('students')
        worker = session['user_id']
        workers = request.form.getlist('workers')
        name = request.form['title']
        description = request.form['description']

        error = None

        if not multiselect:
            error = 'Wybierz chociaz jednego uczestnika kursu.'
        elif not name or len(name) < 3 or len(name) > 45:
            error = 'Nieprawidłowa nazwa kursu (od 3 do 45 znaków)'

        if error is None:
            course_id = insert_course(name, description)
            add_students_to_course(course_id, multiselect)
            add_worker_to_course(course_id, worker)
            for worker_other in workers:
                add_worker_to_course(course_id, worker_other)
            flash('Pomyślnie dodano kurs i jego uczestników!')
            return redirect(url_for("views.index"))

        flash(error)

    worker_faculty = get_user_faculty(session['user_id'])
    students = get_all_students_from_faculty(worker_faculty)
    workers = get_all_workers_from_faculty(worker_faculty, session['user_id'])
    return render_template('courses/add_course.html', students=students, workers=workers)

@bp.route("/delete-course/<int:id>")
@login_required
def delete_course(id):
    delete_course_by_id(id)
    flash("Pomyślnie usunięto kurs.")
    return redirect(url_for('courses.show_courses'))

@bp.route("/courses")
@login_required
def show_courses():
    courses = get_user_courses(session['user_id'])
    return render_template("courses/all_courses.html", courses=courses)

@bp.route("/course/<int:id>")
@login_required
def show_course_info(id):
    students = get_course_students(id)
    return render_template("courses/show_course_info.html", students=students, cid=id, title=get_course_name(id))

@bp.route("/course/<int:cid>/delete-student/<int:uid>")
@login_required
def delete_student(cid,uid):
    delete_student_from_course(cid,uid)
    flash("Pomyślnie usunięto uczestnika kursu.")
    return redirect(url_for('courses.show_course_info', id=cid))

@bp.route("/course/<int:cid>/grades/<int:uid>", methods=['GET', 'POST'])
@login_required
def show_user_grades(cid,uid):
    if request.method == "POST":
        mark = request.form['mark']
        insert_mark(mark, session['user_id'], uid, cid)
        flash("Pomyślnie dodano ocenę")
    avg_mark = get_avg_mark(uid,cid)
    title = 'Oceny - ' + get_user_name(uid) + ' \n z przedmiotu ' + get_course_name(cid)[0]
    marks = get_user_marks_from_course(uid,cid)
    if avg_mark is None:
        avg_mark = 'Brak ocen'
    return render_template("courses/show_grades.html", title=title, marks=marks, avg_grade=avg_mark, cid=cid, uid=uid)

@bp.route("/course/<int:cid>/grades/<int:uid>/delete/<int:gid>")
@login_required
def delete_grade(cid,uid,gid):
    delete_mark(gid)
    flash("Pomyślnie usunięto ocenę.")
    return redirect(url_for('courses.show_user_grades', cid=cid, uid=uid))
