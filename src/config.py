from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
DB_HOST_ = os.environ.get('DB_HOST_')
PORT_ = os.environ.get('PORT_')
TELEGRAM_API_URL = os.environ.get('TELEGRAM_API_URL')
