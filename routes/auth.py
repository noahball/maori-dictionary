"""
auth.py
Noah Ball, June 2024
This file contains our authentication routes.
"""

# Import the necessary modules
from flask import render_template, redirect, request, session
from lib import globals, db, helpers, flask_server

# Import the bcrypt object created when initialising the Flask app
bcrypt = flask_server.bcrypt


# TODO: Signup error handling
# TODO: Check data length and format. Strip all data.

# /login (Log In Page) route
def login_page():
    if helpers.user_authenticated():  # Check if the user is already logged in
        return redirect('/')  # Redirect to the home page

    if request.method == 'POST':  # If the form is submitted (POST request)
        # Strip all data to remove leading/trailing whitespace.
        # Usernames are always stored in lowercase. This is to prevent case sensitivity issues.
        username = request.form['username'].strip().lower()  # Retrieve the username from the form
        password = request.form['password'].strip()  # Retrieve the password from the form
        # TODO: Only retrieve necessary values from the database.
        query = "SELECT * FROM user WHERE username = ?"  # Query to retrieve the user data from the database
        conn = db.create_connection(globals.DATABASE_FILE)  # Create a connection to the database
        cur = conn.cursor()  # Create a cursor object
        cur.execute(query, (username,))  # Execute the query
        user_data = cur.fetchone()  # Retrieve the user data
        conn.close()  # Close the connection

        if user_data is None:  # If the user does not exist
            return redirect(
                '/login?error=Invalid+username+or+password')  # Redirect to the login page with an error message

        try:  # Try to retrieve the user data
            user_id = user_data[0]  # Retrieve the user id
            name = user_data[1]  # Retrieve the user's full name
            username = user_data[2]  # Retrieve the username
            db_password = user_data[3]  # Retrieve the hashed password
            user_type = user_data[4]  # Retrieve the user type
        except IndexError:  # If the user data is not in the correct format/not found
            return redirect(
                '/login?error=Invalid+username+or+password')  # Redirect to the login page with an error message

        if not bcrypt.check_password_hash(db_password, password):  # Check if the password is correct, if incorrect...
            return redirect(
                '/login?error=Invalid+username+or+password')  # Redirect to the login page with an error message

        # Store the user data in the session
        session['user_id'] = user_id  # Store the user id
        session['username'] = username  # Store the username
        session['name'] = name  # Store the user's full name
        session['user_type'] = user_type  # Store the user type

        return redirect('/')  # Redirect to the home page

    return render_template('login.html',
                           error=request.args.get('error'))  # Render the login page with an error message if present


# /signup (Sign Up Page) route
def signup_page():
    if helpers.user_authenticated():  # Check if the user is already logged in
        return redirect('/')  # Redirect to the home page

    if request.method == 'POST':  # If the form is submitted (POST request)
        # Strip all data to remove leading/trailing whitespace.
        name = request.form['name'].strip()  # Retrieve the user's full name from the form
        username = request.form['username'].strip().lower()  # Retrieve the username from the form
        password = request.form['password'].strip()  # Retrieve the password from the form
        confirm_password = request.form['confirm_password'].strip()  # Retrieve the password confirmation from the form

        # Check if the two passwords match
        if password != confirm_password:  # If the passwords do not match
            return redirect(
                '/signup?error=Passwords+do+not+match')  # Redirect to the sign up page with an error message

        # Hash the password using Bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Check if user with username already exists
        conn = db.create_connection(globals.DATABASE_FILE)  # Create a connection to the database
        query = "SELECT id FROM user WHERE username = ?"  # Query to retrieve the user data from the database
        # We only need to check if the user exists, so we only retrieve the user id
        cur = conn.cursor()  # Create a cursor object
        cur.execute(query, (username,))  # Execute the query
        user_data = cur.fetchone()  # Retrieve the user data
        conn.close()  # Close the connection

        if user_data is not None:  # If the user already exists
            return redirect(
                '/signup?error=Username+is+already+taken')  # Redirect to the sign up page with an error message

        query = "INSERT INTO user (name, username, password, type) VALUES (?, ?, ?, ?)"  # Query to insert the new user into the database
        conn = db.create_connection(globals.DATABASE_FILE)  # Create a connection to the database
        cur = conn.cursor()  # Create a cursor object
        cur.execute(query, (name, username, hashed_password, 1))  # Execute the query
        # All new users are created as students (type 1)
        # They can be promoted to a teacher (type 2) by another teacher later on.
        conn.commit()  # Commit the changes to the database
        conn.close()  # Close the connection

        return redirect('/login')  # Redirect to the login page

    return render_template('signup.html',
                           error=request.args.get('error'))  # Render the sign up page with an error message if present


# /logout (Log Out Page) route
def logout_page():
    session.clear()  # Erase the session
    return redirect('/login')  # Redirect to the login page
