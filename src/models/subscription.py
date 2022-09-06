from peewee import DeferredForeignKey, Model

from models import db


class Subscription(Model):
    """
    Subscription model.
    Just a join table for User-User relationship.
    """

    # id field will be created by ORM
    source = DeferredForeignKey("User", backref="subscribed_to")
    target = DeferredForeignKey("User", backref="subscribed_by")

    class Meta:
        db_table = "subscriptions"
        database = db
        # Adding unique constraint to both field to avoid duplicates.
        indexes = ((("source", "target"), True),)
