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
    program = db.Column(db.String(100))
    year = db.Column(db.String(100))
    creditsCompleted = db.Column(db.Float, nullable = False)
    creditsToGraduate = db.Column(db.Float, nullable = False)
    gpa = db.Column(db.Float)
    courses = db.relationship("Course", backref="student")


    def __init__(self, firstName, lastName, email, password, school, program, year, creditsToGraduate):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.school = school
        self.program = program
        self.year = year
        self.creditsCompleted = 0.0
        self.creditsToGraduate = creditsToGraduate


    def __repr__(self):
        return '<Student %r>' % self.email


    def toDict(self):
        return {
            "id": self._id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "school": self.school,
            "program": self.program,
            "year": self.year,
            "creditsCompleted": self.creditsCompleted,
            "creditsToGraduate": self.creditsToGraduate,
            "gpa": self.gpa,
            "courses": self.courses
        }


    def validateAndHashPassword(password: str, confirmPassword: str):
        if (len(password) < 5):
            raise Exception("Password must be more than 4 characters")

        passwordHash = bcrypt.generate_password_hash(password)

        if bcrypt.check_password_hash(passwordHash, confirmPassword):
            return passwordHash
        raise Exception("Passwords do not match")


    def register(first, last, email, password, school, program, year, creditsToGraduate):

        # check that email is valid
        email_regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]\
        +)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+\
        /-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

        if not re.match(email_regex, email):
            raise Exception("Invalid Email")

        found = Student.query.filter_by(email = email).first()
        if not found:

            hashed_password = bcrypt.generate_password_hash(password)
            acc = Student(first, last, email, hashed_password, school, program, year, creditsToGraduate)
            db.session.add(acc)
            db.session.commit()


    def login(email, password):

        student = Student.query.filter_by(email = email).first()

        if not student:
            raise Exception("Email is either invalid or not registered in the system")

        if not bcrypt.check_password_hash(student.password, password):
            raise Exception("Invalid Password")

        fName = student.firstName
        return fName


    def getStudentByEmail(email):
        return Student.query.filter_by(email = email).first()
    
    def calculate(student_id):
        student = Student.query.filter_by(_id = student_id).first()

        sumOfGradePoints = 0

        for course in student.courses:
            sumOfGradePoints += course.gradePoint

        student.gradePoint = sumOfGradePoints / student.creditsCompleted
        db.session.commit()

    def updateStudent(email: str, studentValues: dict):
        student = Student.query.filter_by(email = email).first()
        if "email" in studentValues:
            student.email = studentValues["email"]
        elif "password" in studentValues:
            student.password = studentValues["password"]
        else:
            student.firstName = studentValues["firstName"]
            student.lastName = studentValues["lastName"]
            student.school = studentValues["school"]
        db.session.commit()


    def addCourse(course_code, course_name, student_email, course_credits):
        student = Student.query.filter_by(email = student_email).first()
        course = Course(course_code, course_name, student._id, course_credits)

        student.creditsCompleted += float(course_credits)

        db.session.add(course)
        db.session.commit()
    

    def removeCourse(course_id):
        
        trashed_course = Course.query.filter_by(_id = course_id).first()
        trashed_course.trashed = True
        #Course.query.filter_by(_id = course_id).delete()
        db.session.commit()


    def deleteStudent(email: str):
        student = Student.query.filter_by(email = email).first()
        db.session.delete(student)
        db.session.commit()


class Course(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    code = db.Column(db.String(100), nullable = False)
    name =  db.Column(db.String(100), nullable = False)
    studentId = db.Column(db.Integer, db.ForeignKey("student.id"), nullable = False)
    credits = db.Column(db.Float)
    gradePoint = db.Column(db.Float)
    trashed = db.Column(db.Boolean, default = False, nullable = False) 


    def __init__(self, code, name, studentId, credits):
        self.code = code
        self.name = name
        self.studentId = studentId
        self.credits = credits

    def getCourseById(id):
        return Course.query.filter_by(_id = id, trashed = False).first()


    def calculate(course_Id):
        course = Course.query.filter_by(_id = course_Id, trashed = False).first()
        evaluations = Evaluation.getEvaluations(course_Id)

        sumOfWeights = 0
        sumOfGrades = 0

        for e in evaluations:
            sumOfWeights += e.weight
            sumOfGrades += (e.weight * e.grade)
            
        finalGrade = sumOfGrades/sumOfWeights

        course.gradePoint = Course.convertGradePoint(finalGrade*100)
        db.session.commit()
            
    def convertGradePoint(grade): 

        if (grade >= 93):
            return 4.0
        elif (grade >= 90):
            return 3.7
        elif (grade >= 87):
            return 3.3
        elif (grade >= 83):
            return 3.0
        elif (grade >= 80):
            return 2.7
        elif (grade >= 77):
            return 2.3
        elif (grade >= 73):
            return 2.0
        elif (grade >= 70):
            return 1.7
        elif (grade >= 67):
            return 1.3
        elif (grade >= 65):
            return 1.0
        else:
            return 0.0

    def getCourses(student_email):
        student_id = Student.query.filter_by(email = student_email).first()._id

        return Course.query.filter_by(studentId = student_id, trashed = False)

    def addEvaluation(evaluation_name, evaluation_grade, evaluation_weight, course_id):
        evaluation = Evaluation(evaluation_name, evaluation_grade, evaluation_weight, course_id)

        db.session.add(evaluation)
        db.session.commit()

        course = Course.query.filter_by(_id = course_id).first()

        Course.calculate(course_id)
        Student.calculate(Student.query.filter_by(_id = course.studentId).first()._id)

        return evaluation


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
