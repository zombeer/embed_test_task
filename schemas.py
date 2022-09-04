from datetime import date, datetime

from pydantic import BaseModel


class OrmModel(BaseModel):
    class Config:
        orm_mode = True


class Post(OrmModel):
    id: int | None = None
    title: str
    text: str
    timestamp: datetime
    is_new: bool = False


class User(OrmModel):
    id: int | None = None
    name: str
    password: str | None
    country: str | None = None
    city: str | None = None
    birthDate: date | None = None
    interests: list[str] = []
    bio: str = ""
    posts: list[Post] = []
    subscriptions: list[str] = []
    subscribers_count: int = 0
    subscriptions_count: int = 0
    last_login: datetime | None = None


class GenericApiResponse(BaseModel):
    code: int
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str
