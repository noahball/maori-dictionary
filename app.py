from lib import flask_server
from routes import pages

app = flask_server.app

app.add_url_rule('/', 'home_page', view_func=pages.home_page)
app.add_url_rule('/category/<cat_id>', 'category_page', view_func=pages.category_page)
app.add_url_rule('/login', 'login_page', methods=['GET', 'POST'], view_func=pages.login_page)
app.add_url_rule('/signup', 'signup_page', methods=['GET', 'POST'],view_func=pages.signup_page)
app.add_url_rule('/logout', 'logout_page', view_func=pages.logout_page)

if __name__ == '__main__':
    app.run()
