from flask import session

from lib import db
from lib import globals


def get_categories():
    query = "SELECT id, name FROM category"
    conn = db.create_connection(globals.DATABASE_FILE)
    cur = conn.cursor()
    cur.execute(query)
    categories = cur.fetchall()
    conn.close()
    return categories

def user_authenticated():
    return 'user_id' in session