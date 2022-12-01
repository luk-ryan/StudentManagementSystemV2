from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)
app.secret_key = "Hello World!"

# Automatically reload server when template files are changed
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Directories for the home page
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# Directory for login page
@app.route("/login")
def login():
    return render_template("login.html")

# Directory for register page
@app.route("/register", methods = ["POST","GET"])
def register():

    # When the user clicks the submit button, it will post it back to /register page
    if request.method == "POST":
        first_name = request.form["fName"] # temporary stores first name field
        session["student_session"] = first_name # stores the above field in session
        flash(f" Logged in Successfully!") # messaging tells user they have been logged in
        return redirect(url_for("student")) # redirects to student page

    # Default register page 
    else:
        return render_template("register.html")

# Directory for the Student page
@app.route("/student")
def student():

    # this is the default Student home page once they log in
    if "student_session" in session:
        s = session["student_session"]
        return render_template("student.html", student = s)
    
    # redirects back to login if they are not logged in the session
    else:
        flash(f"You are not logged in")
        return redirect(url_for("login"))

# Log out of a session
@app.route("/logout")
def logout():

    # messaging to let user know they have been logged out
    if "student_session" in session:
        s = session["student_session"]
        flash(f" {s} has been logged out Successfully", "info")

    session.pop("student_session", None)    
    return redirect(url_for("login"))