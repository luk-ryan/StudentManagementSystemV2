from flask_sqlalchemy import SQLAlchemy
from backend import app

db = SQLAlchemy(app)
class students(db.Model):
   id = db.Column(db.Integer)
   name = db.Column(db.String())
   email = db.Column(db.String(), unique = True)
   school = db.Column(db.String())
