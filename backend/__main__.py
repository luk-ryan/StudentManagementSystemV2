from backend import app
from backend.models import *
from backend.controllers import *

"""
This file runs the server at a given port
"""

FLASK_PORT = 8081

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=FLASK_PORT, host='0.0.0.0')