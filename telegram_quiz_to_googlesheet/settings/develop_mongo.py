from telegram_quiz_to_googlesheet.settings.base import *

from pymongo import MongoClient
from pymongo.database import Database

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', None)
if DEBUG is None:
    DEBUG = False
else:
    if 'true' == DEBUG.lower():
        DEBUG = True
    else:
        DEBUG = False


ALLOWED_HOSTS = ["*"]

MONGO_CLIENT = MongoClient('mongodb://localhost:27017/')
MONGO_DB: Database = MONGO_CLIENT.mongo_db_file

# from pymongo.collection import Collection
# collection: Collection = MONGO_DB.mongo_collection
