"""
flask_server.py
Noah Ball, June 2024
This file initialises our Flask app object with Bcrypt.
"""

# Importing the necessary modules
from flask import Flask
from flask_bcrypt import Bcrypt

from lib import globals # Import our global environment variables

app = Flask(__name__, template_folder='../templates', static_folder='../static') # Create a Flask app object
# We have to manually define our folders because flask_server.py is nested inside the lib folder
bcrypt = Bcrypt(app) # Create a Bcrypt object
app.secret_key = globals.SECRET_KEY # Set the secret key for our sessions
