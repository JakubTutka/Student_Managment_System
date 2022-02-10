from flaskext.mysql import MySQL
import time
import datetime
mysql = MySQL()


def get_all_students_from_faculty(id):
    cursor = mysql.get_db().cursor()
    cursor.execute(
        "SELECT user_id, first_name, last_name, email FROM users WHERE type_of_user='Student' AND faculty_id=%s", (id,))
    students = cursor.fetchall()
    return students

def get_all_workers_from_faculty(id, creator_id=0):
    cursor = mysql.get_db().cursor()
    cursor.execute(
        "SELECT user_id, first_name, last_name, email, degree FROM users WHERE user_id !=%s AND type_of_user='Pracownik' AND faculty_id=%s", (creator_id, id))
    workers = cursor.fetchall()
    return workers

def get_user_faculty(user_id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT faculty_id FROM users WHERE user_id=%s", (user_id,))
    faculty_id = cursor.fetchone()
    return faculty_id

def insert_course(name, description, creator_id):
    cursor = mysql.get_db().cursor()
    cursor.execute(
        "INSERT INTO courses (name, description,creator_id) VALUES (%s, %s, %s)", (name, description, creator_id))
    mysql.get_db().commit()
    cursor.execute(
        "SELECT course_id FROM courses ORDER BY course_id DESC LIMIT 1 ")
    course_id = cursor.fetchone()
    return course_id

def add_worker_to_course(course_id, worker_id):
    cursor = mysql.get_db().cursor()
    cursor.execute(
        "INSERT INTO user_courses (course_id, user_id, role) VALUES (%s, %s, 'Pracownik')", (course_id, worker_id))
    mysql.get_db().commit()

def add_students_to_course(course_id, students):
    cursor = mysql.get_db().cursor()
    for student_id in students:
        cursor.execute(
            "INSERT INTO user_courses (course_id, user_id, role) VALUES (%s, %s, 'Student')", (course_id, student_id))
        mysql.get_db().commit()

def get_user_name(id):
    cursor = mysql.get_db().cursor()
    cursor.execute(
        "SELECT first_name, last_name FROM users where user_id=%s", (id,))
    user = cursor.fetchone()
    return user[0] + ' ' + user[1]

def get_user_email(id):
    cursor = mysql.get_db().cursor()
    cursor.execute(
        "SELECT email FROM users where user_id=%s", (id,))
    email = cursor.fetchone()
    return email

def get_user_courses(id):
    cursor = mysql.get_db().cursor()
    cursor.execute(
        "SELECT c.course_id, c.name, c.description, c.creator_id FROM courses c INNER JOIN user_courses uc USING (course_id) WHERE user_id=%s", (id,))
    courses = cursor.fetchall()
    return courses

def get_course_students(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT u.user_id, u.first_name, u.last_name, u.email FROM users u INNER JOIN user_courses uc USING (user_id) WHERE course_id=%s AND role='Student'", (id,))
    students = cursor.fetchall()
    return students

def get_course_workers(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT u.user_id, u.first_name, u.last_name, u.email FROM users u INNER JOIN user_courses uc USING (user_id) WHERE course_id=%s AND role='Pracownik'", (id,))
    workers = cursor.fetchall()
    return workers

def get_course_name(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT name,description FROM courses WHERE course_id=%s", (id,))
    name = cursor.fetchone()
    return name

def get_faculty_name(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT name_full FROM faculties WHERE faculty_id=%s", (id,))
    name = cursor.fetchone()
    return name

def get_user_marks_from_course(uid,cid):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT mark_id, value, date, u.first_name, u.last_name FROM student_marks, users u WHERE professor_id=u.user_id AND course_id=%s AND student_id=%s", (cid,uid))
    marks = cursor.fetchall()
    return marks

def get_avg_mark(uid,cid):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT avg(value_number) FROM student_marks WHERE student_id=%s AND course_id=%s", (uid,cid))
    avg_mark = cursor.fetchall()
    return avg_mark[0]

def insert_mark(value, pid, uid, cid):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    cursor = mysql.get_db().cursor()
    value_number = get_number_from_grade(value)
    cursor.execute("INSERT INTO student_marks (value, value_number, date,student_id,course_id,professor_id) VALUES (%s, %s, %s, %s, %s, %s)", (value, value_number, timestamp, uid, cid, pid))
    mysql.get_db().commit()

def get_number_from_grade(value):
    return {
        '5.0': 5,
        '4.5': 4.5,
        '4.0' : 4,
        '3.5': 3.5,
        '3.0': 3,
        '2.0': 2
    }[value]

def delete_course_by_id(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("DELETE FROM courses WHERE course_id=%s", (id,))
    mysql.get_db().commit()

def delete_user_from_course(cid, uid):
    cursor = mysql.get_db().cursor()
    cursor.execute("DELETE FROM user_courses WHERE user_id=%s AND course_id=%s", (uid, cid))
    mysql.get_db().commit()

def delete_mark(gid):
    cursor = mysql.get_db().cursor()
    cursor.execute("DELETE FROM student_marks WHERE mark_id=%s",(gid,))
    mysql.get_db().commit()

def get_students_not_in_course(cid,fid):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT user_id, first_name, last_name, email from users WHERE type_of_user='Student' AND faculty_id=%s AND user_id NOT IN (SELECT user_id FROM user_courses WHERE course_id=%s)", (fid,cid))
    students = cursor.fetchall()
    return students

def get_workers_not_in_course(cid,fid):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT user_id, first_name, last_name, email from users WHERE type_of_user='Pracownik' AND faculty_id=%s AND user_id NOT IN (SELECT user_id FROM user_courses WHERE course_id=%s)", (fid,cid))
    workers = cursor.fetchall()
    return workers

def update_course(cid, title, description):
    cursor = mysql.get_db().cursor()
    cursor.execute("UPDATE courses SET name=%s, description=%s WHERE course_id=%s", (title, description, cid))
    mysql.get_db().commit()

def get_creator_of_course(cid):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT creator_id FROM courses WHERE course_id=%s", (cid,))
    creator = cursor.fetchone()
    return creator

def get_all_faculties():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM faculties")
    faculties = cursor.fetchall()
    return faculties

def get_all_faculty_buildings(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM buildings WHERE faculty_id=%s", (id,))
    buildings = cursor.fetchall()
    return buildings

def get_course_ranking(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT user_id, first_name, last_name, email, (SELECT avg(value_number) FROM student_marks WHERE student_id=user_id) AS 'srednia' FROM users INNER JOIN user_courses uc USING (user_id) WHERE course_id=%s AND role='Student' ORDER BY srednia DESC", (id,))
    students = cursor.fetchall()
    return students