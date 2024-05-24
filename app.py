from flask import Flask
from routes import pages

app = Flask(__name__)

app.add_url_rule('/', 'home_page', view_func=pages.home_page)

if __name__ == '__main__':
    app.run()
