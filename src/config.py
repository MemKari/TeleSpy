import os

from dotenv import load_dotenv

load_dotenv()  # this allows you to take it from the file .env data

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')

settings = [DB_HOST, DB_USER, DB_PASS, DB_PORT, DB_NAME]
if not all([settings]):
    raise ValueError("One or more environment variables are not set")

SECRET = os.environ.get('SECRET')

# Telegram settings
api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
phone = os.environ.get('phone')
