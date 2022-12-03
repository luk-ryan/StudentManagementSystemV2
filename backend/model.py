from flask_sqlalchemy import SQLAlchemy
from backend.app import app

db = SQLAlchemy(app)

class Accounts(db.Model):
   _id = db.Column("id", db.Integer, primary_key = True)
   firstName = db.Column(db.String(100))
   lastName = db.Column(db.String(100))
   fullName = db.Column(db.String(100))
   email = db.Column(db.String(100), unique = True)
   school = db.Column(db.String(100))

   def __init__(self, firstName, lastName, email):
      self.firstName = firstName
      self.lastName = lastName
      self.fullName = firstName, lastName
      self.email = email
