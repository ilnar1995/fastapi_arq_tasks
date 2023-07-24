from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

REDIS_HOST = os.environ.get("REDIS_HOST")
KEEP_RESULT = int(os.environ.get("KEEP_RESULT"))

TIME_CACHE = os.environ.get("TIME_CACHE")

DB_NAME_TEST = os.environ.get("DB_NAME_TEST")

SECRET_AUTH = os.environ.get("SECRET_AUTH")
