import os

from flask import Flask
from dotenv import load_dotenv

from lib import create_connection

app = Flask(__name__)
load_dotenv()

DATABASE_FILE = os.getenv('DB_FILE')


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()
