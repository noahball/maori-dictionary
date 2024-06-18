"""
app.py
Noah Ball, June 2024
This is the main file of the application. It contains the routes for the Flask server.
"""

# Importing the necessary modules
from lib import flask_server # Flask configuration
from routes import pages, auth # Import our routes

app = flask_server.app # Retrieve the Flask app object

# Routes
app.add_url_rule('/', 'home_page', view_func=pages.home_page) # Home page
app.add_url_rule('/category/<cat_id>', 'category_page', view_func=pages.category_page) # Category page
app.add_url_rule('/word/<word_id>', 'word_page', view_func=pages.word_page) # Word details page
app.add_url_rule('/login', 'login_page', methods=['GET', 'POST'], view_func=auth.login_page) # Log in page
app.add_url_rule('/signup', 'signup_page', methods=['GET', 'POST'],view_func=auth.signup_page) # Sign up page
app.add_url_rule('/logout', 'logout_page', view_func=auth.logout_page) # Log out page

if __name__ == '__main__': # Start the server
    app.run()
