import os

# Default database(sqlite3)
DB_FALLBACK_URI = "sqlite:////database/embed_xyz_api_fallback.db"

# Target database, use format as mentioned here:
# https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#connect
# postgres and mysql drivers comes installed in the docker image
DB_URI = os.getenv("DB_URI") or DB_FALLBACK_URI

# Remote url for documentations
REMOTE_URL = os.getenv("REMOTE_URL", "http://localhost:8000")

# How many posts should contain user profile at /users/
POST_PREVIEW_COUNT = os.getenv("POST_PREVIEW_COUNT", 5)

# CORS Settings TODO:
CORS_ENABLED = bool(os.getenv("CORS_ENABLED", False))
