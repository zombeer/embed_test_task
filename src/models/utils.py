from datetime import date

from models import db
from models.post import Post
from models.subscription import Subscription
from models.user import User


def add_user(username: str, password: str) -> User | None:
    """
    Creates and returns new User() or None if user exists.
    """
    user, created = User.get_or_create(name=username, defaults=dict(password=password))
    if created:
        return user
    else:
        return None


def post_filter_query_builder(
    query,
    keyword: str | None = None,
    start: date | None = None,
    end: date | None = None,
):
    """
    Builds filter query to be applied to list posts query.
    User can search his/her posts by the title name via a simple substring match.
    User can search his/her posts by date published via start date and end date filters
    """
    if keyword:
        query = query.where(Post.title.contains(keyword))
    if start:
        query = query.where(Post.created.date() >= start)
    if end:
        query = query.where(Post.created.date() <= end)
    return query


def create_tables():
    """
    Helper to initialize tables
    """
    db.create_tables([User, Post, Subscription])
