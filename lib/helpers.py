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
