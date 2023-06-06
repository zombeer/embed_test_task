from datetime import date, datetime

from pydantic import BaseModel, Field


class MessageSchema(BaseModel):
    """Simply result message."""

    detail: str = Field(..., title="Details of operation")


class PostSchema(BaseModel):
    """Post data shown in list of users post."""

    id: int
    title: str
    text: str
    created: datetime

    class Config:
        """Pydantic config."""

        orm_mode = True
        schema_extra = {
            "example": {
                "id": 3,
                "title": "Best post ever!",
                "text": "Nulla nec porttitor nunc. Duis in quam et arcu convallis sollicitudin sed et eros. Integer auctor posuere dictum. Ut fermentum placerat purus, eget gravida odio faucibus fermentum.",
                "created": "2022-09-06T11:02:55.123Z",
            }
        }


class PostWithAuthorSchema(PostSchema):
    """Post data shown in subscriptions, with post author mentioned/."""

    author: str

    class Config:
        """Pydantic config."""

        orm_mode = True
        schema_extra = {
            "example": {
                "id": 3,
                "title": "Best post ever!",
                "text": "Nulla nec porttitor nunc. Duis in quam et arcu convallis sollicitudin sed et eros. Integer auctor posuere dictum. Ut fermentum placerat purus, eget gravida odio faucibus fermentum.",
                "created": "2022-09-06T11:02:55.123Z",
                "author": "User1",
            }
        }


class UserProfile(BaseModel):
    """User profile public data."""

    name: str
    country: str
    city: str
    birthdate: date | None
    interests: list[str]
    bio: str
    subscriptions: list[str]
    subscribers_count: int
    subscriptions_count: int
    post_count: int

    class Config:
        """Pydantic config."""

        orm_mode = True


class UserProfileWithPosts(UserProfile):
    """User profile data with post samples included."""

    posts: list[PostSchema] = []


class Token(BaseModel):
    """Login token."""

    access_token: str
    token_type: str


class TokenPlus(Token):
    """Login token with user data."""

    message: str
