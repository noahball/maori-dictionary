from flask import render_template
from lib import globals
from lib import db
from lib import helpers

def home_page():
    query = "SELECT id, maori, english, definition, level, category, filename FROM word"
    conn = db.create_connection(globals.DATABASE_FILE)
    cur = conn.cursor()
    cur.execute(query)
    words = cur.fetchall()
    conn.close()

    categories = helpers.get_categories()
    categories = [c[1] for c in categories]
    return render_template('home.html', words=words, categories=categories)
