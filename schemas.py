import re
from datetime import date, datetime

from fastapi import Body
from pydantic import BaseModel, validator


class PostSchema(BaseModel):
    id: int
    title: str
    text: str
    created: datetime

    class Config:
        orm_mode = True


class GenericApiResponse(BaseModel):
    code: int
    message: str


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


class UpdateUserProfilePayload(BaseModel):
    """
    User can update the following parts of his/her profile: short biography, birth date, country, city, list of interests.
    """

    country: str | None = Body(None, title="Users country")
    city: str | None = Body(None, title="Users city")
    birthdate: date | None = Body(None, title="User birth date")
    interests: list[str] = Body([], title="List of user interests")

    class Config:
        schema_extra = {
            "example": {
                "country": "Spain",
                "city": "Madrid",
                "birthdate": "2017-07-21",
                "interests": ["sleep", "code"],
            }
        }

    @validator("interests")
    def validate_interests(cls, v):
        """
        This validator not only validats interests, but also casts list of strings into comma separated string so store it in DB.
        """
        for item in v:
            assert item.isalnum(), "interests must be alpha-numericals"
        return ", ".join(v)


class UserPasswordPayload(BaseModel):
    """
    Username + Password payload for registering and signing in.
    """

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

    class Config:
        schema_extra = {
            "example": {
                "username": "BestUser1",
                "password": "OloloTrolo123#@!",
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str
