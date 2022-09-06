import os

from playhouse.db_url import connect


def get_db():
    db_url = os.getenv("DB_URL") or "sqlite:///embed_xyz_api.db"
    return connect(db_url)


db = get_db()
