from flaskext.mysql import MySQL
mysql = MySQL()


def get_all_students_from_faculty(id):
    cursor = mysql.get_db().cursor()

    cursor.execute(
        "SELECT user_id, first_name, last_name, email FROM users WHERE type_of_user='Student' AND faculty_id=%s", (id,))

    students = cursor.fetchall()

    return students


def get_user_faculty(user_id):

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT faculty_id FROM users WHERE user_id=%s", (user_id,))
    faculty_id = cursor.fetchone()
    return faculty_id

def insert_course(name, description):
    cursor = mysql.get_db().cursor()
    cursor.execute("INSERT INTO courses (name, description) VALUES (%s, %s)", (name, description))
    mysql.get_db().commit()
    cursor.execute("SELECT course_id FROM courses ORDER BY course_id DESC LIMIT 1 ")
    course_id = cursor.fetchone()
    return course_id

def add_worker_to_course(course_id, worker_id):
    cursor = mysql.get_db().cursor()
    cursor.execute("INSERT INTO user_courses (course_id, user_id, role) VALUES (%s, %s, 'Pracownik')", (course_id, worker_id))
    mysql.get_db().commit()

def add_students_to_course(course_id, students):
    cursor = mysql.get_db().cursor()
    for student_id in students:
        cursor.execute("INSERT INTO user_courses (course_id, user_id, role) VALUES (%s, %s, 'Student')", (course_id, student_id))
        mysql.get_db().commit()

def get_user_name(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT first_name, last_name FROM users where user_id=%s", (id,))
    user = cursor.fetchone()
    return user[0] + ' ' + user[1]


def get_user_courses(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT name, description FROM courses c INNER JOIN (SELECT ", (id,))
    courses = cursor.fetchall()
    return courses
