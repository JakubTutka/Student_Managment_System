from flask import Flask, render_template
from . import db_info
from app.database import mysql, get_user_email, get_creator_of_course
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
    app.jinja_env.globals.update(username=get_user_email)
    app.jinja_env.globals.update(get_creator_of_course=get_creator_of_course)
    mysql.init_app(app)

    @app.errorhandler(404)
    def PageNotFound(error):
        return render_template('views/error404.html')

    # registering blueprints
    from . import auth, views, courses, faculties
    app.register_blueprint(views.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(courses.bp)
    app.register_blueprint(faculties.bp)

    return app
