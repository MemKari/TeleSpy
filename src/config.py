import os

from dotenv import load_dotenv

load_dotenv()  # this allows you to take it from the file .env data

# Telegram settings
api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
phone = os.environ.get('phone')
keywords = os.environ.get('keywords')
result_channel_ID = int(os.environ.get('result_channel_ID', 123))

