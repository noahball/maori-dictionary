import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_FILE = os.getenv('DB_FILE')