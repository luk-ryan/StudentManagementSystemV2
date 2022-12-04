from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from backend.models import Student

from backend import app

def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            try:
                student = Student.query.filter_by(email=email).one_or_none()
                if student:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(student)
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner


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


@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html', message='')


@app.route("/register", methods = ["POST"])
def register_post():
    first_name = request.form["fName"] # temporary stores first name field
    last_name = request.form["lName"]
    email = request.form["email"]
    session["name"] = first_name # stores the above field in session

    try:
        Student.register(first_name, last_name, email)
        flash(f"Logged in Successfully!") # messaging tells user they have been logged in
        return redirect(url_for("student")) # redirects to student page
    except:
        flash(f"Invalid email")
        return redirect(url_for("student"))


@app.route("/registerInvalid")
def register_invalid():
    return redirect(url_for("register_get"))



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
    
    return render_template("view.html", values = Student.query.all())
