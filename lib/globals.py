"""
globals.py
Noah Ball, June 2024
This file configures our global environment variables.
"""

# Import the necessary modules
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Update the DATABASE_FILE and SECRET_KEY variables with those from the .env file or our system
DATABASE_FILE = os.getenv('DATABASE_FILE')
SECRET_KEY = os.getenv('SECRET_KEY')