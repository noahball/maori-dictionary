"""
globals.py
Noah Ball, June 2024
This file contains our helper functions.
"""

# Import the necessary modules
from flask import session

from lib import db, globals  # Import our database functions and global environment variables


def get_categories():
    """ Retrieve all categories from the database
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
