from flask import render_template
from lib import globals
from lib import db


def home_page():
    return render_template('home.html')
