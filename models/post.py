from datetime import datetime

from peewee import CharField, DateTimeField, DeferredForeignKey, Model, TextField

from models import db

# from models.user import User


class Post(Model):
    """
    Post model
    """

    # id field will be created by ORM
    author = DeferredForeignKey("User", backref="posts")
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
