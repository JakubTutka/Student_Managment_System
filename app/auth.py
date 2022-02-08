import functools
from flask import (
    Blueprint, redirect, render_template, request, url_for, flash, session, logging
)
import time
import datetime
from .database import mysql
from werkzeug.security import (check_password_hash, generate_password_hash)

bp = Blueprint("auth", __name__)


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_id') is None:
            return redirect(url_for("auth.sign_in"))

        return view(**kwargs)

    return wrapped_view


@bp.route('/sign-in', methods=('POST', 'GET'))
def sign_in():
    cursor = mysql.get_db().cursor()
    if request.method == "POST":
        email = request.form['email']
        password = request.form["password"]

        error = None

        cursor.execute(
            "SELECT user_id, email, password, type_of_user FROM users WHERE email=%s", (email,))

        user = cursor.fetchone()

        if user is None or not check_password_hash(user[2], password):
            error = "Nieprawidłowa nazwa użytkownika bądź hasło."

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            session['user_type'] = user[3]
            session.permanent = True
            flash("Pomyslnie zalogowano")
            return redirect(url_for("views.index"))

        flash(error)
    return render_template('auth/sign_in.html')


@bp.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(
        ts).strftime('%Y-%m-%d %H:%M:%S')
    cursor = mysql.get_db().cursor()

    if request.method == 'POST':
        fname = request.form['first_name'].strip()
        lname = request.form['last_name'].strip()
        password = request.form['password']
        email = get_user_email(fname, lname, 'student')
        faculty_id = request.form['faculty']
        error = None

        if not fname or len(fname) < 3 or len(fname) > 45:
            error = 'Nieprawidłowe imię (od 3 do 45 znaków)'
        elif not lname or len(lname) < 3 or len(lname) > 45:
            error = 'Nieprawidłowe nazwisko (od 3 do 45 znaków)'
        elif not password or len(password) < 8 or len(password) > 45:
            error = 'Nieprawidlowe hasło (od 8 do 45 znaków)'

        if error is None:
            cursor.execute("INSERT INTO users (email, password, first_name, last_name, creation_date, type_of_user, degree, faculty_id) VALUES (%s, %s, %s, %s, %s, 'Student', 'Brak', %s)",
                           (email, generate_password_hash(password), fname, lname, timestamp, faculty_id))
            mysql.get_db().commit()
            flash('Pomyślnie zajerestrowano! Twój adres email to: ' + email)
            return redirect(url_for("views.index"))

        flash(error)

    cursor.execute("SELECT faculty_id, name_short, name_full FROM faculties")
    faculties = cursor.fetchall()

    return render_template('auth/sign_up.html', faculties=faculties)


@bp.route('/create-worker-account', methods=('POST', 'GET'))
def create_worker_accounr():
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(
    ts).strftime('%Y-%m-%d %H:%M:%S')
    cursor = mysql.get_db().cursor()

    if request.method == 'POST':
        fname = request.form['first_name'].strip()
        lname = request.form['last_name'].strip()
        password = request.form['password']
        email = get_user_email(fname, lname, 'pracownik')
        degree = request.form['degree']
        faculty_id = request.form['faculty']
        error = None

        if not fname or len(fname) < 3 or len(fname) > 45:
            error = 'Nieprawidłowe imię (od 3 do 45 znaków)'
        elif not lname or len(lname) < 3 or len(lname) > 45:
            error = 'Nieprawidłowe nazwisko (od 3 do 45 znaków)'
        elif not password or len(password) < 8 or len(password) > 45:
            error = 'Nieprawidlowe hasło (od 8 do 45 znaków)'

        if error is None:
            cursor.execute("INSERT INTO users (email, password, first_name, last_name, creation_date, type_of_user, degree, faculty_id) VALUES (%s, %s, %s, %s, %s, 'Pracownik', %s, %s)",
                           (email, generate_password_hash(password), fname, lname, timestamp, degree, faculty_id))
            mysql.get_db().commit()
            flash('Pomyślnie zajerestrowano! Twój adres email to: ' + email)
            return redirect(url_for("views.index"))

        flash(error)

    cursor.execute("SELECT faculty_id, name_short, name_full FROM faculties")
    faculties = cursor.fetchall()
    return render_template('auth/create_worker_account.html', faculties=faculties) 



@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.index'))

def get_user_email(first_name, last_name,type):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT create_email(%s, %s,%s)", (first_name, last_name, type))
    result = cursor.fetchone()
    email = result[0].lower()

    return email
