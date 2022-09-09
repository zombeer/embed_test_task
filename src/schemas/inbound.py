import re
from datetime import date

from fastapi import Body, Query
from pydantic import BaseModel, validator


class UpdateUserProfilePayload(BaseModel):
    """
    User can update the following parts of his/her profile: short biography, birth date, country, city, list of interests.
    """

    country: str | None = Body(None, title="Users country")
    city: str | None = Body(None, title="Users city")
    bio: str | None = Body(None, title="Users shoty biography")
    birthdate: date | None = Body(None, title="User birth date")
    interests: list[str] = Body([], title="List of user interests")

    class Config:
        schema_extra = {
            "example": {
                "country": "Spain",
                "city": "Madrid",
                "birthdate": "1984-07-21",
                "bio": "Let's talk about yourself...",
                "interests": ["sleep", "code"],
            }
        }

    @validator("interests")
    def validate_interests(cls, v):
        """
        This validator not only validates interests, but also casts list of strings into comma separated string so store it in DB.
        """
        for item in v:
            assert item.isalnum(), "interests must be alpha-numericals"
        return ", ".join(v)


class Username(BaseModel):
    """
    Basic username field with validator.
    """

    username: str = Body(..., title="Unique name of the user")

    @validator("username")
    def validate_username(cls, v):
        assert v.isalnum(), "Username must contain only letters or numbers"
        assert len(v) < 15, "Username length must be less than 15 symbols"
        assert len(v) > 3, "Username length must be more than 3 symbols"
        return v

    class Config:
        schema_extra = {
            "example": {
                "username": "BestUser1",
            }
        }


class LoginPayload(Username):
    """
    Username + Password payload for registering and signing in.
    """

    password: str = Body(..., title="Password for the new user")

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


class PostFilterPayload(BaseModel):
    """
    Values for posts and subscription post filtration.
    """

    keyword: str | None = Query(None, title="Keyword to loop up in post title")
    start: date | None = Query(None, title="Post shoud be created after this date")
    end: date | None = Query(None, title="Post should be created before this date")

    class Config:
        schema_extra = {
            "example": {
                "keyword": "keyword",
                "start": "2020-09-06",
                "end": "2022-09-06",
            }
        }


class NewPostPayload(BaseModel):
    """
    Payload for adding new post.
    """

    title: str = Body(..., title="Title of the new post")
    text: str = Body(..., title="Text of the new post")

    @validator("title")
    def validate_title(cls, v):
        assert 1 < len(v) < 100, "Post title should 1 to 100 characters long"
        return v

    @validator("text")
    def validate_text(cls, v):
        assert 10 < len(v) < 1000, "Post text should 10 to 1000 characters long"
        return v

    class Config:
        schema_extra = {
            "example": {
                "title": "Best post title ever!",
                "text": "Some lorem ipsum text which is even better than post title!",
            }
        }
