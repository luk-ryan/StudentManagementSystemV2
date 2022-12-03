'''
an init file is required for this folder to be considered as a module
'''
from flask import Flask
import os

package_dir = os.path.dirname(
    os.path.abspath(__file__)
)

templates = os.path.join(
    package_dir, "templates"
)

template_folder = os.path.abspath(
    os.path.join(os.path.dirname( __file__ ), '..', 'frontend', 'templates')
)

static_folder = os.path.abspath(
    os.path.join(os.path.dirname( __file__ ), '..', 'frontend', 'static')
)

app = Flask(
    __name__,
    template_folder=template_folder,
    static_folder=static_folder
)

db_string = os.getenv('db_string')

if db_string:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_string
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '69cae04b04756f65eabcd2c5a11c8c24'
app.app_context().push()
