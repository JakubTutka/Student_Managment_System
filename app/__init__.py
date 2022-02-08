from flask import Flask,session
from . import db_info
from .database import mysql, get_user_name
from datetime import timedelta

def create_app():

    # create and configure the app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'you-will-never-guess'
    app.config['MYSQL_DATABASE_USER'] = db_info.dbuser
    app.config['MYSQL_DATABASE_PASSWORD'] = db_info.dbpass
    app.config['MYSQL_DATABASE_DB'] = db_info.dbname
    app.config['MYSQL_DATABASE_HOST'] = db_info.dbhost
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
    app.jinja_env.globals.update(username=get_user_name)
    mysql.init_app(app)

    # registering blueprints
    from . import auth, views, courses
    app.register_blueprint(views.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(courses.bp)

    return app
