"""
pages.py
Noah Ball, June 2024
This file contains our routes for viewing categories and words.
"""

# Import the necessary modules
from flask import render_template, redirect, session, request
from lib import db, helpers


# Define our routes

# / (Home page) route
def home_page():
    if not helpers.user_authenticated():  # Check if the user is logged in
        return redirect('/login')  # If not, redirect to the login page

    # Retrieve all words from the database
    words = db.run_query("SELECT id, maori, english, definition, level, category, filename FROM word", (), True, False)

    categories = helpers.get_categories()  # Retrieve all categories from the database for the sidebar
    # Render the home page, passing the words and categories to the template
    return render_template('home.html', words=words, categories=categories, session=session, error=request.args.get("error"), cat_name="All Words")


# /category/<cat_id> (Category page) route
def category_page(cat_id):
    if not helpers.user_authenticated():  # Check if the user is logged in
        return redirect('/login')  # If not, redirect to the login page

    # Validate category id is an int
    try:
        cat_id = int(cat_id)
    except ValueError:
        return redirect('/?error=Category+ID+is+invalid.')

    # Check if the category id provided is valid and grab the category name
    cat_name = db.run_query("SELECT name FROM category WHERE id = ?", (cat_id,), False, False)

    if cat_name is None:  # If the category id is invalid
        return redirect('/?error=Category+not+found')  # Redirect to the home page
    else:
        cat_name = cat_name[0] # Retrieve the category name from the tuple

    # Retrieve all words from the database that match the category id provided
    words = db.run_query("SELECT id, maori, english, definition, level, category, filename FROM word WHERE category = ?", (cat_id,), True, False)

    categories = helpers.get_categories()  # Retrieve all categories from the database for the sidebar

    # Render the category page, passing the words in the category and sidebar categories to the template
    return render_template('home.html', words=words, cat_id=cat_id, cat_name=cat_name, error=request.args.get("message"), categories=categories)


# /word/<word_id> (Word details page) route
def word_page(word_id):
    if not helpers.user_authenticated():  # Check if the user is logged in
        return redirect('/login')  # If not, redirect to the login page

    # Validate word id is an int
    try:
        word_id = int(word_id) # Convert to int
    except ValueError:
        return redirect('/?=Word+ID+is+invalid.') # Redirect to the home page with an error message

    # Retrieve the word from the database that matches the word id provided
    # Query to retrieve a single word
    word = db.run_query("SELECT id, maori, english, definition, level, category, filename FROM word WHERE id = ?", (word_id,), False, False)

    if word is None:  # If the word id is invalid
        return redirect('/?error=Word+not+found')  # Redirect to the home page with an error message

    # Get the category name for the word
    cat_name = db.run_query("SELECT name FROM category WHERE id = ?", (word_id,), False, False)

    if cat_name is None:
        return redirect('/?error=Category+for+word+not+found')
    else:
        cat_name = cat_name[0]

    categories = helpers.get_categories()  # Retrieve all categories from the database for the sidebar
    # Render the word details page, passing the word and sidebar categories to the template
    return render_template('word.html', word=word, cat_name=cat_name, categories=categories)

# /add_word (Add word page) route
def add_word_page(cat_id):
    if not helpers.user_authenticated():  # Check if the user is logged in
        return redirect('/login')  # If not, redirect to the login page

    if request.method == 'POST':  # If the form is submitted (POST request)
        # Check data exists
        if 'maori' not in request.form or 'english' not in request.form or 'definition' not in request.form or 'level' not in request.form:
            return redirect('/add-word/' + cat_id + '?error=Please+fill+in+all+fields.') # Redirect to the add word page with an error message

        # Strip all data to remove leading/trailing whitespace
        maori = request.form['maori'].strip()
        english = request.form['english'].strip()
        definition = request.form['definition'].strip()
        level = request.form['level'].strip()
        if 'filename' in request.form: # Filename is optional
            filename = request.form['filename'].strip()
        else:
            filename = None

        # Check if the data is valid
        # We are only validating length because of issues caused by macrons in the regex
        """
        Māori:
        - 1-35 characters long
        English:
        - 1-35 characters long
        Definition:
        - 1-256 characters long # Increased from 35 to 256 in original database
        
        Filename:
        - 1-35 characters long
        
        Level:
        - Is an integer
        
        Category ID:
        - Is a valid category ID and integer (we do this later)
        """

        # Validate māori, english, and definition
        if not helpers.validate_string_length(maori, 1, 35) or not helpers.validate_string_length(english, 1, 35) or not helpers.validate_string_length(definition, 1, 256):
            return redirect('/add-word/' + cat_id + '?error=Invalid+data+lengths.')

        # Make filename none if it is empty
        if filename == "":
            filename = None
            # Else validate filename if it exists
        elif not helpers.validate_string_length(filename, 1, 35):
            return redirect('/add-word/' + cat_id + '?error=Invalid+data+length+for+image+file.')

        # Validate level
        try :
            level = int(level) # Convert to int
        except ValueError: # If the level is not an integer
            return redirect('/add-word/' + cat_id + '?error=Level must be a number.') # Redirect to the add word page with an error message

    # We exit the if statement to run the following usual validation of our category id

    # Validate category id is an int
    try:
        cat_id = int(cat_id)
    except ValueError:
        return redirect('/add-word/' + cat_id + '/?=Category+ID+is+invalid.')

    # Check if the category id provided is valid and grab the category name
    cat_name = db.run_query("SELECT name FROM category WHERE id = ?", (cat_id,), False, False)

    if cat_name is None:  # If the category id is invalid
        return redirect('/?error=Category+not+found')
    else:
        cat_name = cat_name[0]

    # Re-enter the if statement after our usual validation
    if request.method == 'POST':
        # Insert the word into the database
        db.run_query("INSERT INTO word (maori, english, definition, level, category, filename) VALUES (?, ?, ?, ?, ?, ?)", (maori, english, definition, level, cat_id, filename), False, True)
        return redirect('/category/' + str(cat_id) + '?message=Word+added+successfully.')

    categories = helpers.get_categories()  # Retrieve all categories from the database for the dropdown

    return render_template('add_word.html', cat_id=cat_id, cat_name=cat_name, error=request.args.get("error"), categories=categories)

# /delete_word/<word_id> (Delete word page) route
def delete_word_page(word_id):
    if not helpers.user_authenticated():  # Check if the user is logged in
        return redirect('/login')  # If not, redirect to the login page

    # Validate word id is an int
    try:
        word_id = int(word_id)
    except ValueError:
        return redirect('/?error=Word+ID+is+invalid.')

    # Check if the word id provided is valid
    word_english = db.run_query("SELECT english FROM word WHERE id = ?", (word_id,), False, False)

    if word_english is None:  # If the word id is invalid
        return redirect('/?error=Word+not+found')  # Redirect to the home page with an error message
    else:
        word_english = word_english[0]

    # We are doing this further down because we use the same validation as a GET request
    if request.method == 'POST':  # If the form is submitted (POST request)
        # Check data exists
        if 'confirm' not in request.form or request.form['confirm'] != 'yes':
            return redirect('/delete-word/' + str(word_id) + '?error=Please+tick+the+box+to+confirm+deletion.')

        # Delete the word from the database
        db.run_query("DELETE FROM word WHERE id = ?", (word_id,), False, True)
        return redirect('/?error=' + word_english + '+deleted+successfully.')

    categories = helpers.get_categories()  # Retrieve all categories from the database for the sidebar

    # Render the delete word page with the necessary parameters
    return render_template('delete_word.html', word_id=word_id, word_english=word_english, error=request.args.get("error"), categories=categories)