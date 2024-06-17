from flask import render_template, redirect, request, session
from lib import globals
from lib import db
from lib import helpers
from lib import flask_server

bcrypt = flask_server.bcrypt

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
    return render_template('home.html', words=words, categories=categories, session=session)

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
    if request.method == 'POST':
        username = request.form['username'].strip().lower()
        password = request.form['password'].strip()
        query = "SELECT * FROM user WHERE username = ?"
        conn = db.create_connection(globals.DATABASE_FILE)
        cur = conn.cursor()
        cur.execute(query, (username,))
        user_data = cur.fetchone()
        conn.close()

        try:
            user_id = user_data[0]
            name = user_data[1]
            username = user_data[2]
            db_password = user_data[3]
            user_type = user_data[4]
        except IndexError:
            return redirect('/login?error=Invalid+username+or+password')

        if not bcrypt.check_password_hash(db_password, password):
            return redirect('/login?error=Invalid+username+or+password')

        session['user_id'] = user_id
        session['username'] = username
        session['name'] = name
        session['user_type'] = user_type

        return redirect('/')

    return render_template('login.html')

def signup_page():
    if request.method == 'POST':
        name = request.form['name'].strip()
        username = request.form['username'].strip().lower()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()

        if password != confirm_password:
            return redirect('/signup?error=Passwords+do+not+match')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Check if user with username already exists
        conn = db.create_connection(globals.DATABASE_FILE)
        query = "SELECT * FROM user WHERE username = ?"
        cur = conn.cursor()
        cur.execute(query, (username,))
        user_data = cur.fetchone()
        conn.close()

        if user_data is not None:
            return redirect('/signup?error=Username+already+exists')

        query = "INSERT INTO user (name, username, password, type) VALUES (?, ?, ?, ?)"
        conn = db.create_connection(globals.DATABASE_FILE)
        cur = conn.cursor()
        cur.execute(query, (name, username, hashed_password, 1))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('signup.html')