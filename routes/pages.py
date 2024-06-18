"""
pages.py
Noah Ball, June 2024
This file contains our routes for viewing categories and words.
"""

# Import the necessary modules
from flask import render_template, redirect, session
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
    return render_template('home.html', words=words, categories=categories, session=session)


# /category/<cat_id> (Category page) route
def category_page(cat_id):
    if not helpers.user_authenticated():  # Check if the user is logged in
        return redirect('/login')  # If not, redirect to the login page

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
    return render_template('home.html', words=words, categories=categories)


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

    categories = helpers.get_categories()  # Retrieve all categories from the database for the sidebar
    # Render the word details page, passing the word and sidebar categories to the template
    return render_template('word.html', word=word, categories=categories)
