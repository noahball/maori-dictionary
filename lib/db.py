"""
db.py
Noah Ball, June 2024
This file contains the function used to connect to the database and to run queries.
"""

# Importing the necessary modules
import sqlite3
from lib import globals


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


def run_query(query: str, params: tuple, multiple: bool, commit: bool):
    """ Run a query on the database
    Parameters:
        query (str): The query to run
        params (tuple): The parameters to pass to the query
        multiple (bool): Whether the query returns multiple rows
        commit (bool): Whether to commit the query
    Returns:
        The result of the query
    """
    conn = create_connection(globals.DATABASE_FILE)  # Create a connection to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute(query, params)  # Execute the query

    if commit:  # If the query requires a commit
        conn.commit()  # Commit the query

    if multiple:  # If the query returns multiple rows
        result = cur.fetchall()  # Retrieve all rows
    else:  # If the query returns a single row
        result = cur.fetchone()  # Retrieve the row
    conn.close()  # Close the connection
    return result  # Return the result
