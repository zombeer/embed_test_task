from datetime import datetime

from peewee import (
    CharField,
    DateField,
    DateTimeField,
    ForeignKeyField,
    Model,
    TextField,
)
from playhouse.hybrid import hybrid_property

from database import db


class User(Model):
    """
    Database User model
    """

    name = CharField(15, primary_key=True)
    password = CharField()
    country = CharField(default="")
    city = CharField(default="")
    birthdate = DateField(null=True)
    _interests = TextField(default="", column_name="interests")
    bio = TextField(default="")
    last_activity = DateTimeField(null=True)

    class Meta:
        db_table = "users"
        database = db

    @hybrid_property
    def interests(self):
        """Get list of user interests from a comma separated string."""
        return [x.strip() for x in self._interests.split(",")]

    @hybrid_property
    def subscribers_count(self) -> int:
        return self.subscribed_by.count()

    @hybrid_property
    def subscriptions_count(self) -> int:
        return self.subscribed_to.count()

    @hybrid_property
    def post_count(self) -> int:
        return len(self.posts)

    @hybrid_property
    def subscriptions(self) -> list[str]:
        return [x.target.name for x in self.subscribed_to]

    def subscribe(self, username: str):
        return Subscription.create(source=self.name, target=username)

    def unsubscribe(self, username: str):
        return Subscription.select().where(source=self.name, target=username).delete()

    def create_post(self, title: str, text: str):
        return Post.create(title=title, text=text, user=self)

    def bump(self):
        """
        Small helper to update last_activity timestamp.
        """
        User.update(last_activity=datetime.now()).where(
            User.name == self.name
        ).execute()


class Post(Model):
    """
    Post model
    """

    # id field will be created by ORM
    user = ForeignKeyField(User, backref="posts")
    title = CharField(100)
    text = TextField()
    created = DateTimeField(default=datetime.now)

    class Meta:
        db_table = "posts"
        database = db


class Subscription(Model):
    """
    Subscription model.
    Just a join table for User-User relationship.
    """

    # id field will be created by ORM
    source = ForeignKeyField(User, backref="subscribed_to")
    target = ForeignKeyField(User, backref="subscribed_by")

    class Meta:
        db_table = "subscriptions"
        database = db
        # Adding unique constraint to both field to avoid duplicates.
        indexes = ((("source", "target"), True),)


def create_user(username: str, password: str) -> User | None:
    """
    Creates and returns new User() or None if user exists.
    """
    user, created = User.get_or_create(name=username, defaults=dict(password=password))
    if created:
        return user
    else:
        return None


def create_tables():
    """Helper to initialize tables"""
    db.create_tables([User, Post, Subscription])
