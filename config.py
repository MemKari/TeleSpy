import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')  # this allows you to take it from the file .env data


api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
phone = os.environ.get('phone')
