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
            course_id = insert_course(name, description, session['user_id'])
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
    creator = get_creator_of_course(id)
    return render_template("courses/show_course_info.html", students=students, cid=id, title=get_course_name(id), creator=creator[0])

@bp.route("/course/<int:id>/ranking")
@login_required
def show_ranking(id):
    students = get_course_ranking(id)
    title = get_course_name(id)
    return render_template("courses/show_course_ranking.html", students=students, title=title)


@bp.route("/course/<int:id>/workers")
@login_required
def show_course_workers(id):
    workers = get_course_workers(id)
    creator = get_creator_of_course(id)
    return render_template("courses/show_course_workers.html", workers=workers, creator=creator[0], cid=id)

@bp.route("/course/<int:cid>/delete-student/<int:uid>")
@login_required
def delete_student(cid, uid):
    delete_user_from_course(cid, uid)
    flash("Pomyślnie usunięto uczestnika kursu.")
    if session['user_type'] == 'Student':
        return redirect(url_for('courses.show_courses'))
    return redirect(url_for('courses.show_course_info', id=cid))

@bp.route("/course/<int:cid>/delete-worker/<int:uid>")
@login_required
def delete_worker(cid,uid):
    delete_user_from_course(cid,uid)
    creator = get_creator_of_course(cid)
    flash("Pomyślnie usunięto uczestnika kursu.")
    if session['user_id'] != creator[0]:
        return redirect(url_for('courses.show_courses'))
    return redirect(url_for('courses.show_course_info', id=cid))

@bp.route("/course/<int:cid>/grades/<int:uid>", methods=['GET', 'POST'])
@login_required
def show_user_grades(cid, uid):
    if request.method == "POST":
        mark = request.form['mark']
        insert_mark(mark, session['user_id'], uid, cid)
        flash("Pomyślnie dodano ocenę")
    avg_mark = get_avg_mark(uid, cid)
    title = 'Oceny - ' + \
        get_user_name(uid) + ' \n z przedmiotu ' + get_course_name(cid)[0]
    marks = get_user_marks_from_course(uid, cid)
    if avg_mark is None:
        avg_mark = 'Brak ocen'
    return render_template("courses/show_grades.html", title=title, marks=marks, avg_grade=avg_mark, cid=cid, uid=uid)


@bp.route("/course/<int:cid>/grades/<int:uid>/delete/<int:gid>")
@login_required
def delete_grade(cid, uid, gid):
    delete_mark(gid)
    flash("Pomyślnie usunięto ocenę.")
    return redirect(url_for('courses.show_user_grades', cid=cid, uid=uid))


@bp.route("/course/<int:cid>/add_user", methods=['POST', 'GET'])
@login_required
def add_user(cid):
    if request.method == "POST":
        students = request.form.getlist('students')
        workers = request.form.getlist('workers')
        add_students_to_course(cid, students)
        for worker in workers:
            add_worker_to_course(cid, worker)
        flash('Pomyślnie dodano nowych uczestników kursu!')
        return redirect(url_for("courses.show_course_info", id=cid))

    faculty_id = get_user_faculty(session['user_id'])
    students = get_students_not_in_course(cid,faculty_id)
    workers = get_workers_not_in_course(cid,faculty_id)
    return render_template('courses/add_user.html', students=students, workers=workers)

@bp.route("/course/<int:cid>/edit", methods=['POST','GET'])
@login_required
def edit_course(cid):
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        update_course(cid, title, description)
        flash("Pomyślnie zedytowano kurs")
        return redirect(url_for("courses.show_course_info", id=cid))
    course = get_course_name(cid)
    return render_template('courses/edit_course.html', course=course)