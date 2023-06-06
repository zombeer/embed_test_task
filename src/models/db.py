from playhouse.db_url import connect

from config import DB_URI


def get_db() -> connect:
    """Returns a database connection."""
    return connect(DB_URI)


db = get_db()
