import os

from config import DB_URI
from playhouse.db_url import connect


def get_db():
    return connect(DB_URI)


db = get_db()
