from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
from flask_sqlalchemy import SQLAlchemy
from backend import app
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
    school = db.Column(db.String(100))
    gpa = db.Column(db.Float)
    courses = db.relationship("Course", backref="student")


    def __init__(self, firstName, lastName, email):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email


    def __repr__(self):
        return '<Student %r>' % self.email


    def register(first, last, email):

        # check that email is valid
        email_regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]\
        +)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+\
        /-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

        if not re.match(email_regex, email):
            raise Exception("Invalid Email")

        found = Student.query.filter_by(email = email).first()
        if not found: 
            acc = Student(first, last, email)
            db.session.add(acc)
            db.session.commit()


    def login(email):

        stud = Student.query.filter_by(email = email).first()

        if not stud:
            raise Exception("Email is either invalid or not registered in the system")
        
        fName = stud.firstName

        return fName


    def addCourse(course_code, course_name, student_email):
        student_id = Student.query.filter_by(email = student_email).first()._id

        course = Course(course_code, course_name, student_id)

        db.session.add(course)
        db.session.commit()
    
    def removeCourse(course_id):
        
        Course.query.filter_by(_id = course_id).delete()
        db.session.commit()


class Course(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    code = db.Column(db.String(100), nullable = False)
    name =  db.Column(db.String(100), nullable = False)
    studentId = db.Column(db.Integer, db.ForeignKey("student.id"), nullable = False)
    gradePoint = db.Column(db.Float)


    def __init__(self, code, name, studentId):
        self.code = code
        self.name = name
        self.studentId = studentId


    def calculate():
        evaluations = Evaluation.query.filter_by(courseId = id)

        for ev in evaluations:
            print(ev)

    def getCourses(student_email):
        student_id = Student.query.filter_by(email = student_email).first()._id

        return Course.query.filter_by(studentId = student_id)


class Evaluation(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name =  db.Column(db.String(100), nullable = False)
    grade = db.Column(db.Float)
    weight = db.Column(db.Float, nullable = False)
    courseId = db.Column(db.Integer, nullable = False)

    def __init__(self, name, grade, weight, courseId):
        self.name = name
        self.grade = grade/100
        self.weight = weight/100
        self.courseId = courseId