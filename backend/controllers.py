import os
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from backend.models import Student, Course, Evaluation, Semester, Event, Course_event
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

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

    if "NAME" in session:
        student = Student.getStudentByEmail(session["EMAIL"])
        return render_template("student.html", student = student)
    else:
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
        return redirect(url_for("home")) # redirects to student page
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

    school = request.form["school"]
    program = request.form["program"]
    year = request.form["year"]
    year_string = "year " + year
    creditsToGraduate = request.form["creditsToGraduate"]

    try:
        Student.register(first_name, last_name, email, password, school, program, year_string, creditsToGraduate)
        flash(f"You have been successfully registered! Please login with your email", "success") # messaging tells user they have been logged in
        return redirect(url_for("login_get")) # redirects to student page
    except Exception as err:
        flash(f"{str(err)}", "error")
        return render_template('register.html', message='', form=request.form)


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


@app.route("/course", methods = ["GET"])
def course_get():

    '''
    Directory for viewing all courses
    '''

    if "NAME" in session:
        student = Student.getStudentByEmail(session["EMAIL"])
        courses = Course.getCourses(session["EMAIL"])
        semesters = Semester.getSemesters(session["EMAIL"])
        return render_template("courses.html", student = student, courses = list(courses), semesters = list(semesters))

    # redirects back to login if they are not logged in the session
    else:
        flash(f"You are not logged in", "error")
        return redirect(url_for("login_get"))


@app.route("/course", methods = ["POST"])
def course_post():

    '''
    Adding Course
    '''

    course_code = request.form["course code"]
    course_name = request.form["course name"]
    course_credits = request.form["credits"]
    course_semesterId = request.form["semester id"]

    Student.addCourse(course_code, course_name, session["EMAIL"], course_credits, course_semesterId)

    return redirect(url_for("course_get"))


@app.route("/semester", methods = ["POST"])
def semester_post():

    '''
    Adding Semester
    '''

    request.get_data()

    display_name = request.form["display name"]
    start_date = request.form["start date"]
    end_date = request.form["end date"]

    try:
        semester = Student.addSemester(display_name, start_date, end_date, session["EMAIL"])
        return {
            "semester_id": semester._id,
            "semester_displayName": semester.displayName
        }, 201
    except Exception as err:
        return str(err), 400


@app.route("/course/<id>", methods = ["GET"])
def course_get_by_id(id):

    '''
    Get course by id
    '''

    course = Course.getCourseById(id)
    evaluations = Evaluation.getEvaluations(course._id)
    events = Event.getEventByCourseId(course._id)
    courseEvents = Course_event.getCourseEventByCourseId(course._id)

    return render_template(
        'course.html',
        course = course,
        student = session["NAME"],
        evaluations = evaluations,
        events = events,
        courseEvents = courseEvents
    )


@app.route("/course/<id>", methods = ["DELETE"])
def course_delete(id):

    '''
    Deleting course
    '''

    Student.removeCourse(request.view_args["id"])

    return "success"


@app.route("/evaluation", methods = ["POST"])
def evaluation_post():

    '''
    Adding evaluation
    '''

    request.get_data()

    evaluation_name = request.json["evaluation_name"]
    evaluation_grade = request.json["evaluation_grade"]
    evaluation_weight = request.json["evaluation_weight"]
    course_id = request.json["course_id"]

    evaluation = Course.addEvaluation(evaluation_name, evaluation_grade, evaluation_weight, course_id)

    return {
        "evaluation_name": evaluation.name,
        "evaluation_grade": evaluation.grade,
        "evaluation_weight": evaluation.weight
    }, 201


@app.route("/event", methods = ["POST"])
def event_post():

    '''
    Adding event
    '''

    request.get_data()

    event_name = request.form["name"]
    event_category = request.form["category"]
    event_start_date = request.form["start_date"]
    event_end_date = request.form["end_date"]
    event_start_time = request.form["start_time"]
    event_end_time = request.form["end_time"]
    course_id = request.form["course_id"]
    
    event = Course.addEvent(event_name, event_category, event_start_date, event_end_date, event_start_time, event_end_time, course_id)
    return redirect(url_for("course_get_by_id", id = course_id))
    
    
@app.route("/courseEvent", methods = ["POST"])
def course_event_post():
    
    '''
    Adding course event
    '''

    request.get_data()

    course_event_name = request.form["name"]
    course_event_category = request.form["category"]
    course_event_day = request.form["day"]
    course_event_start_time = request.form["start_time"]
    course_event_end_time = request.form["end_time"]
    course_id = request.form["course_id"]
    
    courseEvent = Course.addCourseEvent(course_event_name, course_event_category, course_event_day, course_event_start_time, course_event_end_time, course_id)
    return redirect(url_for("course_get_by_id", id = course_id))
    

@app.route("/profile", methods = ["GET"])
def profile_get():
    '''
    Render the student's profile page.
    '''

    if "EMAIL" in session:
        student = Student.getStudentByEmail(session["EMAIL"])
        return render_template("profile.html", student = student)
    else:
        flash(f"You are not logged in", "error")
        return redirect(url_for("login_get"))


@app.route("/student", methods = ["POST"])
@app.route("/student/email", methods = ["POST"])
def update_profile():
    '''
    Update a student's first name, last name, and/or school.
    '''

    if "EMAIL" in session:
        Student.updateStudent(session["EMAIL"], request.form)

        if "email" in request.form:
            session["EMAIL"] = request.form["email"]
            flash(f"Email updated", "success")
        else:
            flash(f"Profile updated", "success")
        return redirect(url_for("profile_get"))
    else:
        flash(f"You are not logged in", "error")
        return redirect(url_for("login_get"))


@app.route("/student/avatar", methods = ["POST"])
def upload_profile_picture():
    if "EMAIL" in session:
        try:
            if "file" not in request.files:
                flash("No file found in form", "error")
                return redirect(url_for("profile_get"))

            file = request.files["file"]

            if file.filename == "":
                flash("No file uploaded", "error")
                return redirect(url_for("profile_get"))

            if "." not in file.filename:
                flash("Invalid filename: no file extension", "error")
                return redirect(url_for("profile_get"))

            filename_extension = file.filename.rsplit(".", 1)[1].lower()

            if filename_extension == "jpg":
                filename_extension = "jpeg"

            allowable_file_types = ["png", "jpg", "jpeg", "gif"]

            if filename_extension not in allowable_file_types:
                flash("Invalid file type. Allowed types: " + str(allowable_file_types), "error")
                return redirect(url_for("profile_get"))

            if "image/" + filename_extension != file.mimetype:
                flash("File extension does not match its mimetype", "error")
                return redirect(url_for("profile_get"))

            student = Student.getStudentByEmail(session["EMAIL"])

            # Make the avatar folder in the file system if it does not already exist.
            # Otherwise, there will be an error when saving the file.
            if not os.path.exists(app.config["AVATAR_UPLOAD_FOLDER"]):
                os.makedirs(app.config["AVATAR_UPLOAD_FOLDER"])

            # If user already has an avatar, delete it
            if student.avatarFilename:
                oldAvatarFilePath = os.path.join(app.config["AVATAR_UPLOAD_FOLDER"], student.avatarFilename)
                if os.path.exists(oldAvatarFilePath):
                    os.remove(oldAvatarFilePath)

            # User's avatar saved as static/images/avatars/<id>.<extension>
            avatarFilename = str(student._id) + "." + filename_extension
            avatarFilePath = os.path.join(app.config["AVATAR_UPLOAD_FOLDER"], avatarFilename)

            file.save(avatarFilePath)

            Student.setAvatarFilename(student.email, avatarFilename)

            flash("Avatar uploaded", "success")
            return redirect(url_for("profile_get"))
        except RequestEntityTooLarge:
            flash("File size too large", "error")
            return redirect(url_for("profile_get"))
    else:
        flash("You are not logged in", "error")
        return redirect(url_for("login_get"))


@app.route("/student/avatar/delete", methods = ["POST"])
def delete_avatar():
    if "EMAIL" in session:
        student = Student.getStudentByEmail(session["EMAIL"])

        os.remove(os.path.join(app.config["AVATAR_UPLOAD_FOLDER"], student.avatarFilename))

        Student.removeAvatarFilename(student.email)

        flash("Avatar deleted", "success")
        return redirect(url_for("profile_get"))
    else:
        flash("You are not logged in", "error")
        return redirect(url_for("login_get"))


@app.route("/student/password", methods = ["POST"])
def change_password():
    '''
    Update a student's first name, last name, and/or school.
    '''

    if "EMAIL" in session:
        student = Student.getStudentByEmail(session["EMAIL"])
        try:
            Student.login(student.email, request.form["currentPassword"])
        except Exception as exception:
            flash("Current password incorrect", "error")
            return redirect(url_for("profile_get"))
        try:
            hashedPassword = Student.validateAndHashPassword(request.form["newPassword"], request.form["confirmNewPassword"])
            Student.updateStudent(session["EMAIL"], { "password": hashedPassword })
        except Exception as exception:
            flash(str(exception), "error")
            return redirect(url_for("profile_get"))

        flash(f"Password updated", "success")
        return redirect(url_for("profile_get"))
    else:
        flash(f"You are not logged in", "error")
        return redirect(url_for("login_get"))


@app.route("/student/delete", methods = ["POST"])
def delete_student():
    '''
    Delete a student from the database.
    '''

    if "EMAIL" in session:
        if session["EMAIL"] == request.form["email"]:
            Student.deleteStudent(request.form["email"])
            del session["EMAIL"]
            del session["NAME"]
            return redirect(url_for("home"))
        else:
            flash("User attempted to be deleted does not match with current session user", "error")
            return redirect(url_for("profile_get"))
    else:
        flash("You are not logged in", "error")
        return redirect(url_for("login_get"))
