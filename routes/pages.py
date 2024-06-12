from flask import render_template
from lib import globals
from lib import db


def home_page():
    query = "SELECT id, maori, english, definition, level, category, filename FROM word"
    conn = db.create_connection(globals.DATABASE_FILE)
    cur = conn.cursor()
    cur.execute(query)
    words = cur.fetchall()
    conn.close()
    return render_template('home.html', words=words)
