from datetime import date, datetime

from pydantic import BaseModel, Field


class MessageSchema(BaseModel):
    detail: str = Field(..., title="Details of operation")


class PostSchema(BaseModel):
    id: int
    title: str
    text: str
    created: datetime

    class Config:
        orm_mode = True


class PostWithAuthorSchema(PostSchema):
    author: str


class UserProfile(BaseModel):
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
        orm_mode = True


class UserProfileWithPosts(UserProfile):
    posts: list[PostSchema] = []


class Token(BaseModel):
    access_token: str
    token_type: str
