from flask import Flask
from routes import pages

app = Flask(__name__)

app.add_url_rule('/', 'home_page', view_func=pages.home_page)
app.add_url_rule('/category/<cat_id>', 'category_page', view_func=pages.category_page)

if __name__ == '__main__':
    app.run()
