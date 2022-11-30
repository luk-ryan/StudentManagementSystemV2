from flask import Flask, render_template
# this is a comment to commit
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/home")
def home():
    return render_template("home.html")