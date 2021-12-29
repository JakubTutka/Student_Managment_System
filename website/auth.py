from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST']) #pozwalanie na metody do formularzy
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # sortowanie po bazce i mailu
        user = User.query.filter_by(email=email).first()
        # sprawdzanie hasła
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # sesja we flasku, ze gosc jest zalogowany
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email does not exist!', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/map')
def map():
    return render_template('map.html', user=current_user)

@auth.route('/grades')
def grades():
    return render_template('grades.html', user=current_user)

@auth.route('/timetable')
def timetable():
    return render_template('timetable.html', user=current_user)

@auth.route('/buildings')
def buildings():
    return render_template('buildings.html', user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)