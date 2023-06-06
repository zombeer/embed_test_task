from datetime import datetime, timezone

from peewee import CharField, DateField, DateTimeField, DoesNotExist, Model, TextField
from playhouse.hybrid import hybrid_property

from exceptions import (
    add_subscription_exception,
    cant_subscribe_to_youserlf,
    subscription_not_found_exception,
    user_not_found_exception,
)
from models import Post, Subscription, db

MAX_SUBSCRIPTIONS = 100


class User(Model):
    """Database User model."""

    name = CharField(15, primary_key=True)
    password = CharField()
    country = CharField(default="")
    city = CharField(default="")
    birthdate = DateField(null=True)
    _interests = TextField(default="", column_name="interests")
    bio = TextField(default="")
    last_activity = DateTimeField(null=True)

    class Meta:
        """Peewee Meta class."""

        table_name = "users"
        database = db

    @hybrid_property
    def interests(self) -> list[str]:
        """Gets list of user interests from a comma separated string stored in DB."""
        return [x.strip() for x in self._interests.split(",")]

    @hybrid_property
    def subscribers_count(self) -> int:
        """Returns the number of subscribers."""
        return self.subscribed_by.count()

    @hybrid_property
    def subscriptions_count(self) -> int:
        """Returns the number of subscriptions."""
        return self.subscribed_to.count()

    @hybrid_property
    def post_count(self) -> int:
        """Returns the number of posts."""
        return len(self.posts)

    @hybrid_property
    def subscriptions(self) -> list[str]:
        """Returns a list of usernames that current user is subscribed to."""
        return [x.target.name for x in self.subscribed_to]

    def add_subscription(self, username: str) -> Subscription:
        """Adds username to self.subscriptons.

        Added an extra check because Sqlite wasn't following foreign key constraints for some reason.
        """
        if self.name == username:
            raise cant_subscribe_to_youserlf
        if self.subscriptions_count >= MAX_SUBSCRIPTIONS:
            raise add_subscription_exception
        target = User.get_or_none(User.name == username)
        if not target:
            raise user_not_found_exception
        return Subscription.insert(source=self, target=target).execute()

    def delete_subscription(self, username: str) -> None:
        """Deletes subscription by username."""
        try:
            subscription = Subscription.get(source=self.name, target=username)
        except DoesNotExist:
            raise subscription_not_found_exception
        Subscription.delete_by_id(subscription.id)

    def add_post(self, title: str, text: str) -> Post:
        """Adds a post to current user."""
        return Post.create(title=title, text=text, author=self)

    def feed(self) -> list[Post]:
        """Posts by current user subscriptions."""
        subquery = Subscription.select(Subscription.target).where(
            Subscription.source == self.name
        )
        return Post.select().where(Post.author.in_(subquery)).order_by(Post.id.desc())

    def bump(self) -> None:
        """Small helper to update last_activity timestamp."""
        User.update(last_activity=datetime.now(tz=timezone.utc)).where(
            User.name == self.name
        ).execute()
