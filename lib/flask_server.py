from flask import Flask
from flask_bcrypt import Bcrypt

from lib import globals

app = Flask(__name__, template_folder='../templates', static_folder='../static')
bcrypt = Bcrypt(app)
app.secret_key = globals.SECRET_KEY