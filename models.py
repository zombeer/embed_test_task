from datetime import date, datetime

from peewee import (
    CharField,
    DateField,
    DateTimeField,
    DoesNotExist,
    ForeignKeyField,
    IntegrityError,
    Model,
    TextField,
)
from playhouse.hybrid import hybrid_property

from database import db
from exceptions import subscription_not_found_exception, user_not_found_exception


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
        """Gets list of user interests from a comma separated string stored in DB."""
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

    def add_subscription(self, username: str):
        """
        Adds username to self.subscriptons.
        Added an extra check because Sqlite wasn't following foreign key constraints for some reason.
        """
        target = User.get_or_none(User.name == username)
        if not target:
            raise user_not_found_exception
        return Subscription.insert(source=self, target=target).execute()

    def delete_subscription(self, username: str):
        try:
            subscription = Subscription.get(source=self.name, target=username)
        except DoesNotExist:
            raise subscription_not_found_exception
        Subscription.delete_by_id(subscription.id)

    def add_post(self, title: str, text: str):
        return Post.create(title=title, text=text, author=self)

    def feed(self):
        """
        Posts by current user subscriptions
        """
        subquery = Subscription.select(Subscription.target).where(
            Subscription.source == self.name
        )
        posts = Post.select().where(Post.author.in_(subquery)).order_by(Post.id.desc())
        return posts

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
    author = ForeignKeyField(User, backref="posts")
    title = CharField(100)
    text = TextField()
    created = DateTimeField(default=datetime.now)

    class Meta:
        db_table = "posts"
        database = db

    def as_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            text=self.text,
            author=self.author.name,
            created=self.created,
        )


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
