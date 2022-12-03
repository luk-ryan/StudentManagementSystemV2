from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Hello World!"

# Automatically reload server when template files are changed
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class accounts(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    fullName = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True)
    school = db.Column(db.String(100))

    def __init__(self, firstName, lastName, email):
        self.firstName = firstName
        self.lastName = lastName
        self.fullName = firstName + " " + lastName
        self.email = email


@app.route("/")
@app.route("/home")
def home():

    '''
    Directories for the home page
    '''

    return render_template("home.html")


@app.route("/login")
def login():

    '''
    Directory for login page
    '''

    return render_template("login.html")


@app.route("/register", methods = ["POST","GET"])
def register():

    '''
    Directory for register page
    '''

    # When the user clicks the submit button, it will post it back to /register page
    if request.method == "POST":
        first_name = request.form["fName"] # temporary stores first name field
        last_name = request.form["lName"]
        e = request.form["email"]
        session["name"] = first_name # stores the above field in session
        
        found = accounts.query.filter_by(email = e).first()
        if found:
            session["email"] = e

        else:
            acc = accounts(first_name, last_name, e)
            db.session.add(acc)
            db.session.commit()

        flash(f" Logged in Successfully!") # messaging tells user they have been logged in
        return redirect(url_for("student")) # redirects to student page

    # Default register page 
    else:
        return render_template("register.html")


@app.route("/student")
def student():
    
    '''
    Directory for the Student page
    '''

    # this is the default Student home page once they log in
    if "name" in session:
        s = session["name"]
        return render_template("student.html", student = s)
    
    # redirects back to login if they are not logged in the session
    else:
        flash(f"You are not logged in")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():

    '''
    Log out of a session
    '''

    # messaging to let user know they have been logged out
    if "name" in session:
        s = session["name"]
        flash(f" {s} has been logged out Successfully", "info")

    session.pop("name", None)
    session.pop("email", None)  
    return redirect(url_for("login"))


@app.route("/view")
def view():

    '''
    Testing purposes for visualizing database
    '''
    
    return render_template("view.html", values = accounts.query.all())


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)