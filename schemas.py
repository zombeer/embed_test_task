import re
from datetime import date, datetime

from fastapi import Body
from pydantic import BaseModel, validator


class OrmModel(BaseModel):
    class Config:
        orm_mode = True


class Post(OrmModel):
    id: int
    title: str
    text: str
    timestamp: datetime
    is_new: bool = False


class User(OrmModel):
    name: str
    password: str | None
    country: str | None = None
    city: str | None = None
    birthdate: date | None = None
    interests: list[str] = []
    bio: str = ""
    posts: list[Post] = []
    subscriptions: list[str] = []
    subscribers_count: int = 0
    subscriptions_count: int = 0
    last_activity: datetime | None = None


class GenericApiResponse(BaseModel):
    code: int
    message: str


class UserPasswordPayload(BaseModel):
    username: str = Body(..., title="Username of new user")
    password: str = Body(..., title="Password for the new user")

    @validator("username")
    def validate_username(cls, v):
        assert v.isalnum(), "Username must contain only letters or numbers"
        assert len(v) < 15, "Username length must be less than 15 symbols"
        assert len(v) > 3, "Username length must be more than 3 symbols"
        return v

    @validator("password")
    def validate_password(cls, v):
        assert len(v) > 8, "Password should be longer than 8 symbols"
        assert bool(re.search(r"\d", v)), "Password must contain at least one digit"
        assert bool(
            re.search(r"[A-Z]", v)
        ), "Password must contain at least one uppercase letter"
        assert bool(
            re.search(r"[!@#$%^&*()_]", v)
        ), "Password must contain at least one symbol out of !@#$%^&*()_"
        return v


class Token(BaseModel):
    access_token: str
    token_type: str
