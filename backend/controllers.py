from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from backend.models import Student, Course

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


@app.route("/login", methods = ["GET"])
def login_get():

    '''
    Directory for login page
    '''

    return render_template("login.html")


@app.route("/login", methods = ["POST"])
def login_post():

    '''
    Directory for login page
    '''
    email = request.form["email"]
    password = request.form["password"]
    
    try:
        student_info = Student.login(email, password)
        # session["ID"] = student_info[0]
        session["NAME"] =  student_info
        session["EMAIL"] =  email
        # print (session["ID"])
        flash(f"Logged in Successfully!", "info") # messaging tells user they have been logged in
        return redirect(url_for("student")) # redirects to student page
    except Exception as error:
        
        flash(str(error), "error") # messaging tells user they have been logged in
        return render_template("login.html")


@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html', message='')


@app.route("/register", methods = ["POST"])
def register_post():
    first_name = request.form["fName"] # temporary stores first name field
    last_name = request.form["lName"]
    email = request.form["email"]
    password = request.form["password"]

    try:
        Student.register(first_name, last_name, email, password)
        flash(f"You have been successfully registered! Please login with your email", "success") # messaging tells user they have been logged in
        return redirect(url_for("login_get")) # redirects to student page
    except Exception as err:
        flash(f"{str(err)}", "error")
        return render_template('register.html', message='')


@app.route("/registerInvalid")
def register_invalid():
    return redirect(url_for("register_get"))


@app.route("/logout")
def logout():

    '''
    Log out of a session
    '''

    # messaging to let user know they have been logged out
    if "NAME" in session:
        name = session["NAME"]
        flash(f" {name} has been logged out Successfully", "info")

    session.pop("NAME", None)
    session.pop("EMAIL", None)
    return redirect(url_for("login_get"))


@app.route("/student")
def student():
    
    '''
    Directory for the Student page
    '''

    # this is the default Student home page once they log in
    if "NAME" in session:
        name = session["NAME"]
        return render_template("student.html", student = name)
    
    # redirects back to login if they are not logged in the session
    else:
        flash(f"You are not logged in", "error")
        return redirect(url_for("login_get"))


@app.route("/course", methods = ["GET"])
def course_get():

    '''
    Directory for modifying course info
    '''

    if "NAME" in session:
        courses = Course.getCourses(session["EMAIL"])
        return render_template("course.html", student = session["NAME"], courses = courses)

    # redirects back to login if they are not logged in the session
    else:
        flash(f"You are not logged in", "error")
        return redirect(url_for("login_get"))


@app.route("/course", methods = ["POST"])
def course_post():

    '''
    Directory for modifying course info
    '''
    course_code = request.form["course code"]
    course_name = request.form["course name"]

    Student.addCourse(course_code, course_name, session["EMAIL"])

    return redirect(url_for("course_get"))


@app.route("/course/<id>", methods = ["DELETE"])
def course_delete(id):

    '''
    Directory for modifying course info
    '''

    Student.removeCourse(request.view_args["id"])

    return "success"
