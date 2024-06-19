"""
pages.py
Noah Ball, June 2024
This file contains our routes for viewing categories and words.
"""

# Import the necessary modules
from flask import render_template, redirect, session, request
from lib import globals, db, helpers


# Define our routes

# / (Home page) route
def home_page():
    if not helpers.user_authenticated():  # Check if the user is logged in
        return redirect('/login')  # If not, redirect to the login page

    # Retrieve all words from the database
    query = "SELECT id, maori, english, definition, level, category, filename FROM word"  # Query to retrieve all words
    conn = db.create_connection(globals.DATABASE_FILE)  # Create a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute(query)  # Execute the query
    words = cur.fetchall()  # Retrieve all words
    conn.close()  # Close the connection

    categories = helpers.get_categories()  # Retrieve all categories from the database for the sidebar
    # Render the home page, passing the words and categories to the template
    return render_template('home.html', words=words, categories=categories, session=session, error=request.args.get("error"), cat_name="All Words")


# /category/<cat_id> (Category page) route
def category_page(cat_id):
    if not helpers.user_authenticated():  # Check if the user is logged in
        return redirect('/login')  # If not, redirect to the login page

    # Check if the category id provided is valid and grab the category name
    query = "SELECT name FROM category WHERE id = ?"  # Query to retrieve the category name
    conn = db.create_connection(globals.DATABASE_FILE)  # Create a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute(query, (cat_id,))  # Execute the query
    cat_name = cur.fetchone()  # Retrieve the category name
    conn.close()  # Close the connection

    if cat_name is None:  # If the category id is invalid
        return redirect('/?error=Category+not+found')  # Redirect to the home page
    else:
        cat_name = cat_name[0] # Retrieve the category name from the tuple

    # Retrieve all words from the database that match the category id provided
    # Query to retrieve all words in a category
    query = "SELECT id, maori, english, definition, level, category, filename FROM word WHERE category = ?"
    conn = db.create_connection(globals.DATABASE_FILE)  # Create a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute(query, (cat_id,))  # Execute the query
    words = cur.fetchall()  # Retrieve all words
    conn.close()  # Close the connection

    categories = helpers.get_categories()  # Retrieve all categories from the database for the sidebar

    # Render the category page, passing the words in the category and sidebar categories to the template
    return render_template('home.html', words=words, cat_name=cat_name, categories=categories)


# /word/<word_id> (Word details page) route
def word_page(word_id):
    if not helpers.user_authenticated():  # Check if the user is logged in
        return redirect('/login')  # If not, redirect to the login page

    # Retrieve the word from the database that matches the word id provided
    # Query to retrieve a single word
    query = "SELECT id, maori, english, definition, level, category, filename FROM word WHERE id = ?"
    conn = db.create_connection(globals.DATABASE_FILE)  # Create a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute(query, (word_id,))  # Execute the query
    word = cur.fetchone()  # Retrieve the word
    conn.close()  # Close the connection

    if word is None:  # If the word id is invalid
        return redirect('/?error=Word+not+found')

    # Get the category name for the word
    query = "SELECT name FROM category WHERE id = ?"  # Query to retrieve the category name
    conn = db.create_connection(globals.DATABASE_FILE)  # Create a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute(query, (word[5],))  # Execute the query
    cat_name = cur.fetchone()  # Retrieve the category name
    conn.close()  # Close the connection

    cat_name = cat_name[0]  # Retrieve the category name from the tuple

    categories = helpers.get_categories()  # Retrieve all categories from the database for the sidebar
    # Render the word details page, passing the word and sidebar categories to the template
    return render_template('word.html', word=word, cat_name=cat_name, categories=categories)
