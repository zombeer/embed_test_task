from fastapi import Depends, FastAPI, Path
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from auth import authenticate_user, create_access_token, decode_jwt, get_password_hash
from exceptions import (
    not_authorized_exception,
    subscription_exists_exception,
    subscription_not_found_exception,
    user_exists_exception,
    user_not_found_exception,
)
from models import IntegrityError, Post, User, add_user, create_tables
from schemas import (
    LoginPayload,
    MessageSchema,
    NewPostPayload,
    PostSchema,
    PostWithAuthorSchema,
    Token,
    UpdateUserProfilePayload,
    Username,
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
    # Update last user activity every time we see a token from him/her
    user.bump()
    return user


@app.post(
    "/signup",
    response_model=Token,
    tags=["Auth"],
    name="Create new user",
)
async def signup(
    payload: LoginPayload,
) -> Token:
    """
    Create new User by providing a username and password.
    """
    payload.password = get_password_hash(payload.password)
    user = add_user(**payload.dict())
    if not user:
        raise user_exists_exception

    access_token = create_access_token(data={"sub": user.name})
    return Token(access_token=access_token, token_type="bearer")


@app.post(
    "/token",
    response_model=Token,
    name="Obtain new token",
    tags=["Auth"],
)
async def login_for_access_token(
    payload: LoginPayload,
) -> Token:
    """
    User login via username/password pair.
    """
    user = authenticate_user(payload.username, payload.password)
    access_token = create_access_token(data={"sub": user.name})
    return Token(access_token=access_token, token_type="bearer")


@app.get(
    "/users",
    response_model=list[UserProfileWithPosts],
    name="List all user profiles with their 5 latest posts.",
    tags=["List users"],
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
    tags=["List users"],
)
async def get_top20_profiles() -> list[UserProfileWithPosts]:
    """
    List top20 users with their recent posts.
    """
    result = []
    # TODO: Add custom ordering - implement popularity score
    for u in User.select().limit(5):
        u.posts = list(u.posts.order_by(Post.id.desc()).limit(5))
        profileWithPosts = UserProfileWithPosts.from_orm(u)
        result.append(profileWithPosts)
    return result


@app.get(
    "/user/me",
    response_model=UserProfile,
    name="Get current User profile data.",
    tags=["User profile"],
)
async def get_user(current_user: User = Depends(get_current_user)) -> UserProfile:
    """
    Gets current User profile data.
    """
    return UserProfile.from_orm(current_user)


@app.put(
    "/user/me",
    response_model=UserProfile,
    name="Update current User profile data",
    tags=["User profile"],
)
async def update_user(
    payload: UpdateUserProfilePayload,
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Updates current User profile data.
    """
    payload_dict = payload.dict(exclude_none=True)
    User.update(**payload_dict).where(User.name == current_user.name).execute()
    return User.get_by_id(current_user.name)


@app.get(
    "/user/{username}",
    response_model=UserProfile,
    name="Get User profile by username",
    tags=["User profile"],
)
async def user_by_username(username: str = Path(..., title="Username of target User.")):
    """
    Gets current User profile data.
    """
    user = User.get_by_id(username)
    return UserProfile.from_orm(user)


@app.post(
    "/user/me/posts",
    name="Create new post by current user",
    tags=["Posts"],
    response_model=PostSchema,
)
async def new_post(
    payload: NewPostPayload,
    current_user: User = Depends(get_current_user),
) -> PostSchema:
    """
    Creates a new post by current User.
    """
    new_post = current_user.add_post(**payload.dict())
    return PostSchema.from_orm(new_post)


@app.get(
    "/user/me/posts",
    name="Posts of the current User",
    tags=["Posts"],
    response_model=list[PostSchema],
)
async def get_current_user_posts(
    current_user: User = Depends(get_current_user),
) -> list[PostSchema]:
    """
    List of current User posts.
    """
    result = []
    for post in list(current_user.posts):
        result.append(PostSchema.from_orm(post))
    return result


@app.get(
    "/user/{username}/posts",
    name="Posts of the target User",
    tags=["Posts"],
    response_model=list[PostSchema],
)
async def get_user_posts_by_username(username: str) -> list[PostSchema]:
    """
    List posts of the user with target username.
    """
    user = User.get_or_none(User.name == username).execute()
    if not user:
        raise user_not_found_exception
    result = []
    for post in list(user.posts):
        result.append(PostSchema.from_orm(post))
    return result


@app.get(
    "/user/me/subscriptions",
    name="Posts of current user subscripte",
    tags=["Subscriptions"],
    response_model=list[PostWithAuthorSchema],
)
async def get_current_user_subscriptions(
    current_user: User = Depends(get_current_user),
) -> list[PostWithAuthorSchema]:
    """
    Lists posts by current user subscriptions.
    It was quite complicated to write proper docstring to this function (:
    """
    result = []

    for p in current_user.feed():
        result.append(PostWithAuthorSchema(**p.as_dict()))
    return result


@app.post(
    "/user/me/subscriptions",
    name="Add subscription",
    tags=["Subscriptions"],
    response_model=MessageSchema,
)
async def subscribe(
    payload: Username,
    current_user: User = Depends(get_current_user),
) -> list[PostWithAuthorSchema]:
    """
    Adds provided username to current user subscriptions.
    """
    try:
        current_user.add_subscription(payload.username)
    except IntegrityError:
        raise subscription_exists_exception
    return MessageSchema(detail="Subscription added succeessfully")


@app.delete(
    "/user/me/subscriptions",
    name="Delete subscription",
    tags=["Subscriptions"],
    response_model=MessageSchema,
)
async def delete_subscription(
    payload: Username,
    current_user: User = Depends(get_current_user),
) -> list[PostSchema]:
    """
    Deletes provided username from current user subscriptions.
    """
    current_user.delete_subscription(payload.username)
    return MessageSchema(detail="Subscription removed succeessfully")
