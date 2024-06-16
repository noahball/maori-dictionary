import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_FILE = os.getenv('DATABASE_FILE')
SECRET_KEY=os.getenv('SECRET_KEY')