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
        return None

    found = Student.query.filter_by(email = email).first()
    if not found:   
        acc = Student(first, last, email)
        db.session.add(acc)
        db.session.commit()
