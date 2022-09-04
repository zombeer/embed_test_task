from copy import copy

from fastapi import Depends, FastAPI, Path
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from auth import authenticate_user, create_access_token, decode_jwt, get_password_hash
from exceptions import (
    not_authorized_exception,
    user_exists_exception,
    user_not_found_exception,
)
from models import Post, User, create_tables, create_user
from schemas import (
    PostSchema,
    Token,
    UpdateUserProfilePayload,
    UserPasswordPayload,
    UserProfile,
    UserProfileWithPosts,
)

create_tables()

app = FastAPI(
    title="Embed.xyz test API",
    description="Some basic user-post CRUD API example...",
    contact={"email": "zombeer@gmail.com"},
    version="0.1.0",
    servers=[{"url": "http://localhost:8000"}],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

user_model_output = {
    "response_model": UserProfile,
    "response_model_exclude_none": True,
    "response_model_exclude": ["password"],
}


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get instance of current User using token payload or raise corresponding exception.
    """
    try:
        payload = decode_jwt(token)
        username = payload.get("sub")
        if username is None:
            raise user_not_found_exception
    except JWTError:
        raise not_authorized_exception
    user = User.get_or_none(name=username)
    if user is None:
        raise not_authorized_exception
    return user


@app.post(
    "/signup",
    response_model=Token,
    tags=["users", "auth"],
    name="Create new user",
)
async def signup(
    payload: UserPasswordPayload,
) -> Token:
    """
    Create new User by providing a username and password.
    """
    payload.password = get_password_hash(payload.password)
    user = create_user(**payload.dict())
    if not user:
        raise user_exists_exception

    access_token = create_access_token(data={"sub": user.name})
    return Token(access_token=access_token, token_type="bearer")


@app.post(
    "/token",
    response_model=Token,
    name="Obtain new token",
    tags=["users", "auth"],
)
async def login_for_access_token(
    payload: UserPasswordPayload,
) -> Token:
    """
    User login via username/password pair.
    """
    user = authenticate_user(payload.username, payload.password)
    access_token = create_access_token(data={"sub": user.name})
    return Token(access_token=access_token, token_type="bearer")


@app.get(
    "/user",
    response_model=UserProfile,
    name="Get current User profile data.",
    tags=["users"],
)
async def get_user(current_user: User = Depends(get_current_user)) -> UserProfile:
    """
    Get current User profile data.
    """
    return UserProfile.from_orm(current_user)


@app.put(
    "/user",
    response_model=UserProfile,
    name="Update current User profile data",
    tags=["users"],
)
async def update_user(
    payload: UpdateUserProfilePayload,
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Update current User profile data.
    """
    payload_dict = payload.dict(exclude_none=True)
    User.update(**payload_dict).where(User.name == current_user.name).execute()
    return User.get_by_id(current_user.name)


@app.get(
    "/user/{username}",
    response_model=UserProfile,
    name="Get User profile by username",
    tags=["users"],
)
async def user_by_username(username: str = Path(..., title="Username of target User.")):
    user = User.get_by_id(username)
    return UserProfile.from_orm(user)


@app.get(
    "/users",
    response_model=list[UserProfileWithPosts],
    name="List all user profiles with their 5 latest posts.",
    tags=["users"],
)
async def get_all_profiles() -> list[UserProfileWithPosts]:
    """
    List of all users + 5 most recent posts
    """
    result = []
    for u in User.select():
        u.posts = list(u.posts.order_by(Post.id.desc()).limit(5))
        profileWithPosts = UserProfileWithPosts.from_orm(u)
        result.append(profileWithPosts)
    return result


@app.get(
    "/users/top",
    response_model=list[UserProfileWithPosts],
    name="List top user profiles with their 5 latest posts.",
    tags=["users"],
)
async def get_top20_profiles() -> list[UserProfileWithPosts]:
    """
    List top20 users with their recent posts.
    """
    result = []
    for u in User.select().limit(5):
        u.posts = list(u.posts.order_by(Post.id.desc()).limit(5))
        profileWithPosts = UserProfileWithPosts.from_orm(u)
        result.append(profileWithPosts)
    return result


@app.get(
    "/user/posts",
    name="Posts of the current user",
    tags=["posts"],
    response_model=list[PostSchema],
)
async def get_user_posts(current_user: User = Depends(get_current_user)) -> list[Post]:
    return []
