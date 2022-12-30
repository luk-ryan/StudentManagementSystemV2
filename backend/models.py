from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
from flask_sqlalchemy import SQLAlchemy
from backend import app, bcrypt
import re
import email
import datetime

'''
This file defines data models and related management logics
'''

db = SQLAlchemy(app)

class Student(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    firstName = db.Column(db.String(100), nullable = False)
    lastName = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    school = db.Column(db.String(100))
    gpa = db.Column(db.Float)
    courses = db.relationship("Course", backref="student")


    def __init__(self, firstName, lastName, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password


    def __repr__(self):
        return '<Student %r>' % self.email


    def register(first, last, email, password):

        # check that email is valid
        email_regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]\
        +)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+\
        /-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

        if not re.match(email_regex, email):
            raise Exception("Invalid Email")

        found = Student.query.filter_by(email = email).first()
        if not found:

            hashed_password = bcrypt.generate_password_hash(password)
            acc = Student(first, last, email, hashed_password)
            db.session.add(acc)
            db.session.commit()


    def login(email, password):

        student = Student.query.filter_by(email = email).first()

        if not student:
            raise Exception("Email is either invalid or not registered in the system")

        if not bcrypt.check_password_hash(student.password, password): # returns False
            raise Exception("Invalid Password")

        fName = student.firstName
        return fName



    def addCourse(course_code, course_name, student_email):
        student_id = Student.query.filter_by(email = student_email).first()._id

        course = Course(course_code, course_name, student_id)

        db.session.add(course)
        db.session.commit()
    
    def removeCourse(course_id):
        
        trashed_course = Course.query.filter_by(_id = course_id).first()
        trashed_course.trashed = True
        #Course.query.filter_by(_id = course_id).delete()
        db.session.commit()


class Course(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    code = db.Column(db.String(100), nullable = False)
    name =  db.Column(db.String(100), nullable = False)
    studentId = db.Column(db.Integer, db.ForeignKey("student.id"), nullable = False)
    gradePoint = db.Column(db.Float)
    trashed = db.Column(db.Boolean, default = False, nullable = False) 


    def __init__(self, code, name, studentId):
        self.code = code
        self.name = name
        self.studentId = studentId

    def getCourseById(id):
        return Course.query.filter_by(_id = id, trashed = False).first()


    def calculate():
        evaluations = Evaluation.query.filter_by(courseId = id)

        for ev in evaluations:
            print(ev)

    def getCourses(student_email):
        student_id = Student.query.filter_by(email = student_email).first()._id

        return Course.query.filter_by(studentId = student_id, trashed = False)

    def addEvaluation(evaluation_name, evaluation_grade, evaluation_weight, course_id):
        evaluation = Evaluation(evaluation_name, evaluation_grade, evaluation_weight, course_id)

        db.session.add(evaluation)
        db.session.commit()


class Evaluation(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name =  db.Column(db.String(100), nullable = False)
    grade = db.Column(db.Float)
    weight = db.Column(db.Float, nullable = False)
    courseId = db.Column(db.Integer, nullable = False)

    def __init__(self, name, grade, weight, courseId):
        self.name = name
        self.grade = float(grade) / 100
        self.weight = float(weight) / 100
        self.courseId = courseId


    def getEvaluations(course_id):
        return Evaluation.query.filter_by(courseId = course_id).all()
