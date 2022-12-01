from flask import Flask, render_template

app = Flask(__name__)

# Automatically reload server when template files are changed
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/home")
def home():
    return render_template("home.html")
