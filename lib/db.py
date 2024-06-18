"""
db.py
Noah Ball, June 2024
This file contains the function used to connect to the databse.
"""

# Importing the necessary modules
import sqlite3


def create_connection(db_file):
    """ Create a connection to the SQLite Database
    Parameters:
        db_file (str): Database file
    Returns:
        A connection to the database
    """
    try:  # Try/except block to handle exceptions
        connection = sqlite3.connect(db_file)  # Create a connection to the database
        return connection  # Return the connection
    except sqlite3.Error as e:
        print(e)  # Print the error (if one is caught)
    return None
