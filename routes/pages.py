from flask import render_template, redirect
from lib import globals
from lib import db
from lib import helpers

def home_page():
    if not helpers.user_authenticated():
        return redirect('/login')

    query = "SELECT id, maori, english, definition, level, category, filename FROM word"
    conn = db.create_connection(globals.DATABASE_FILE)
    cur = conn.cursor()
    cur.execute(query)
    words = cur.fetchall()
    conn.close()

    categories = helpers.get_categories()
    return render_template('home.html', words=words, categories=categories)

def category_page(cat_id):
    if not helpers.user_authenticated():
        return redirect('/login')

    query = "SELECT id, maori, english, definition, level, category, filename FROM word WHERE category = ?"
    conn = db.create_connection(globals.DATABASE_FILE)
    cur = conn.cursor()
    cur.execute(query, (cat_id,))
    words = cur.fetchall()
    conn.close()

    categories = helpers.get_categories()
    return render_template('home.html', words=words, categories=categories)

def login_page():
    return render_template('login.html')

def signup_page():
    return render_template('signup.html')