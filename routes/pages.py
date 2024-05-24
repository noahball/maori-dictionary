from lib import globals
from lib import db


def home_page():
    db.create_connection(globals.DATABASE_FILE)
    return 'Hello, World!'
