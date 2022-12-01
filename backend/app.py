from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Automatically reload server when template files are changed
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Directories for the home page
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# Directory for login page
@app.route("/login", methods = ["POST","GET"])
def login():
    return render_template("login.html")

# Directory for register page
@app.route("/register")
def register():
    return render_template("register.html")

# Directory for the Student page
@app.route("/student")
def student():
    return render_template("student.html")