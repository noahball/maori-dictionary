"""
auth.py
Noah Ball, June 2024
This file contains our authentication routes.
"""

# Import the necessary modules
from flask import render_template, redirect, request, session
from lib import db, helpers, flask_server

# Import the bcrypt object created when initialising the Flask app
bcrypt = flask_server.bcrypt


# TODO: Signup error handling
# TODO: Check data length and format. Strip all data.

# /login (Log In Page) route
def login_page():
    if helpers.user_authenticated():  # Check if the user is already logged in
        return redirect('/')  # Redirect to the home page

    if request.method == 'POST':  # If the form is submitted (POST request)
        # Check data exists
        if 'username' not in request.form or 'password' not in request.form:
            return redirect('/login?error=Please+fill+in+all+fields.')

        # Strip all data to remove leading/trailing whitespace.
        # Usernames are always stored in lowercase. This is to prevent case sensitivity issues.
        username = request.form['username'].strip().lower()  # Retrieve the username from the form
        password = request.form['password'].strip()  # Retrieve the password from the form

        # Check if the username and password are valid
        # We do this validation here to prevent unnecessary database queries.
        """
        Usernames:
        - 2-16 characters long
        - no _ or . at the beginnning
        - no __ or _. or ._ or .. inside
        - can contain a-z, A-Z, 0-9, _ and .
        - no _ or . at the end
        
        Passwords:
        - must be between eight and 64 characters long
        - must contain at least one letter and one number
        """
        if helpers.validate_string_regex(username, r'^(?=.{2,16}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$') is False or helpers.validate_string_regex(password, r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,64}$') is False:
            return redirect('/login?error=Invalid+username+or+password')

        user_data = db.run_query("SELECT id, name, username, password, type FROM user WHERE username = ?", (username,), False, False)  # Retrieve the user data from the database

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
        # Check data exists
        if 'name' not in request.form or 'username' not in request.form or 'password' not in request.form or 'confirm_password' not in request.form:
            return redirect('/signup?error=Please+fill+in+all+fields.')

        # Strip all data to remove leading/trailing whitespace.
        name = request.form['name'].strip()  # Retrieve the user's full name from the form
        username = request.form['username'].strip().lower()  # Retrieve the username from the form
        password = request.form['password'].strip()  # Retrieve the password from the form
        confirm_password = request.form['confirm_password'].strip()  # Retrieve the password confirmation from the form

        # Check if the name, username, password, and password confirmation are valid
        # We do this validation here to prevent unnecessary database queries.
        """
        Names:
        - 2-30 characters long
        - accept a-z, A-Z, and spaces
        - accept , . ' - characters
        - no leading or trailing spaces
        
        Usernames:
        - 2-16 characters long
        - no _ or . at the beginnning
        - no __ or _. or ._ or .. inside
        - can contain a-z, A-Z, 0-9, _ and .
        - no _ or . at the end

        Passwords:
        - must be between eight and 64 characters long
        - must contain at least one letter and one number
        """

        # We will validate separately for each field to provide more specific error messages.

        # Validate the name
        if helpers.validate_string_regex(name, r'^[a-zA-Z ,.\'-]+$') is False:
            return redirect('/signup?error=Invalid+name.+Please+use+only+letters+and+spaces.')

        # Validate the username
        if helpers.validate_string_regex(username, r'^(?=.{2,16}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$') is False:
            return redirect('/login?error=Invalid+username.+Please+use+2-16+characters+with+only+letters,+numbers,+_+and+.')

        # Validate the password
        if helpers.validate_string_regex(password, r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,64}$') is False:
            return redirect('/signup?error=Invalid+password.+Please+use+8-64+characters+with+at+least+one+letter+and+one+number.')

        # Check if the two passwords match
        if password != confirm_password:  # If the passwords do not match
            return redirect(
                '/signup?error=Passwords+do+not+match')  # Redirect to the sign up page with an error message

        # Hash the password using Bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Check if user with username already exists
        user_data = db.run_query("SELECT id FROM user WHERE username = ?", (username,), False, False)  # Retrieve the user data from the database

        if user_data is not None:  # If the user already exists
            return redirect(
                '/signup?error=Username+is+already+taken')  # Redirect to the sign up page with an error message

        # Insert the new user into the database
        db.run_query("INSERT INTO user (name, username, password, type) VALUES (?, ?, ?, ?)", (name, username, hashed_password, 1), False, True)
        # All new users are created as students (type 1)
        # They can be promoted to a teacher (type 2) by another teacher later on.

        return redirect('/login')  # Redirect to the login page

    return render_template('signup.html',
                           error=request.args.get('error'))  # Render the sign up page with an error message if present


# /logout (Log Out Page) route
def logout_page():
    session.clear()  # Erase the session
    return redirect('/login')  # Redirect to the login page
