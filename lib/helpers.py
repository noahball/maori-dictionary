"""
globals.py
Noah Ball, June 2024
This file contains our helper functions.
"""

# Import the necessary modules
from flask import session
import re

from lib import db, globals  # Import our database functions and global environment variables


def get_categories():
    """ Retrieve all categories from the database for the sidebar
    Parameters:
    Returns:
        A list of all categories in the categories table
    """
    query = "SELECT id, name FROM category"
    conn = db.create_connection(globals.DATABASE_FILE)
    cur = conn.cursor()
    cur.execute(query)
    categories = cur.fetchall()
    conn.close()
    return categories


def user_authenticated():
    """ Check if a user is logged in
    Parameters:
    Returns:
        The user's id if they are logged in, otherwise None
    """
    return 'user_id' in session


def validate_string_length(field: str, min_length: int, max_length: int):
    """ Validate a string based on its length
    Parameters:
        field (str): The field to validate
        min_length (int): The minimum length of the field
        max_length (int): The maximum length of the field
    Returns:
        True if the field is valid, otherwise False
    """
    return min_length <= len(field) <= max_length


def validate_string_regex(field: str, regex: str):
    """ Validate a string based on a regular expression
    Parameters:
        field (str): The field to validate
        regex (str): The regular expression to match against
    Returns:
        True if the field is valid, otherwise False
    """
    return re.match(regex, field) is not None

def get_category_names(words: tuple, categories: tuple):
    """ Add the category name to each word tuple
    Parameters:
        words (tuple): A tuple of word tuples
        categories (tuple): A tuple of category tuples
    Returns:
        A list of word tuples with the category name added
    """
    # Add the category name to each word tuple
    for i in range(len(words)): # For each word
        for j in range(len(categories)): # For each category
            if words[i][5] == categories[j][0]: # If the category ID matches
                words[i] = words[i] + (categories[j][1],) # Add the category name to the word tuple
                break # Break the loop
        if len(words[i]) == 6: # If the category name was not added
            # This means that the category ID was not found, so add "Unknown" to the word tuple
            words[i] = words[i] + ("Unknown",)
    return words

def cat_id_to_name(cat_id: int, categories: tuple):
    """ Convert a category ID to a category name
    Parameters:
        cat_id (int): The category ID to convert
        categories (tuple): A tuple of category tuples
    Returns:
        The category name for the category ID provided
    """
    for i in range(len(categories)): # For each category
        if categories[i][0] == cat_id: # If the category ID matches
            return categories[i][1] # Return the category name
    return "Unknown" # If the category ID is not found, return "Unknown".
    # We only use this for displaying the name to the user, so returning Unknown instead of None is fine.
    # ... and this means less manipulation later on.