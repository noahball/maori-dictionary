from flask import Flask
from lib import globals
from routes import pages

app = Flask(__name__)
app.secret_key = globals.SECRET_KEY

app.add_url_rule('/', 'home_page', view_func=pages.home_page)
app.add_url_rule('/category/<cat_id>', 'category_page', view_func=pages.category_page)
app.add_url_rule('/login', 'login_page', view_func=pages.login_page)
app.add_url_rule('/signup', 'signup_page', view_func=pages.signup_page)
if __name__ == '__main__':
    app.run()
