from datetime import date

from models import Post, Subscription, User, db


def add_user(username: str, password: str) -> User | None:
    """Creates and returns new User() or None if user exists."""
    user, created = User.get_or_create(name=username, defaults={"password": password})
    if created:
        return user
    return None


def post_filter_query_builder(
    query,
    keyword: str | None = None,
    start: date | None = None,
    end: date | None = None,
):
    """Builds filter query to be applied to list posts query.

    User can search his/her posts by the title name via a simple substring match.
    User can search his/her posts by date published via start date and end date filters.
    """
    if keyword:
        query = query.where(Post.title.contains(keyword))
    if start:
        query = query.where(Post.created.date() >= start)
    if end:
        query = query.where(Post.created.date() <= end)
    return query


def get_top_users(limit: int = 20) -> list[User]:
    """Custom rating implemented as sum of user subscribers count and posts count."""
    raw_query = f"""
        SELECT u.*, COUNT(scores.x) AS score
        FROM users u
        LEFT JOIN (
            SELECT author_id AS author, title AS x from posts
            UNION
            SELECT target_id, source_id from subscriptions
            ) scores ON scores.author = u.name
        GROUP BY u.name
        ORDER BY score DESC
        LIMIT {limit}
    """
    return User.raw(raw_query)


def create_tables() -> None:
    """Helper to initialize tables."""
    db.create_tables([User, Post, Subscription])
