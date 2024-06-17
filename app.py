from lib import flask_server
from routes import pages, auth

app = flask_server.app

app.add_url_rule('/', 'home_page', view_func=pages.home_page)
app.add_url_rule('/category/<cat_id>', 'category_page', view_func=pages.category_page)
app.add_url_rule('/word/<word_id>', 'word_page', view_func=pages.word_page)
app.add_url_rule('/login', 'login_page', methods=['GET', 'POST'], view_func=auth.login_page)
app.add_url_rule('/signup', 'signup_page', methods=['GET', 'POST'],view_func=auth.signup_page)
app.add_url_rule('/logout', 'logout_page', view_func=auth.logout_page)

if __name__ == '__main__':
    app.run()
