import sqlite3


def create_connection(db_file):
    """ Create a connection to the SQLite Database
    Parameters:
        db_file (str): Database file
    Returns:
        A connection to the database
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        print(e)
    return None