from exceptions import user_exists_exception
from fastapi import APIRouter
from models import Post
from models.utils import add_user
from schemas.inbound import LoginPayload
from schemas.outbound import Token, TokenPlus
from server.utils import authenticate_user, create_access_token, get_password_hash

auth_router = APIRouter(
    tags=["Auth"],
)


@auth_router.post(
    "/signup",
    response_model=Token,
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


@auth_router.post(
    "/token",
    response_model=TokenPlus,
    name="Obtain new token",
)
async def login_for_access_token(
    payload: LoginPayload,
) -> Token:
    """
    User login via username/password pair.
    """
    user = authenticate_user(payload.username, payload.password)
    access_token = create_access_token(data={"sub": user.name})

    new_posts_query = Post.select()

    # Getting new posts count since last activity of user
    if last_activity := user.last_activity:
        new_posts_query = new_posts_query.where(Post.created > last_activity).where(
            Post.author.in_(user.subscriptions)
        )
    new_post_count = new_posts_query.count()

    return TokenPlus(
        access_token=access_token,
        token_type="bearer",
        message=f"You have {new_post_count} new posts from your subscriptions.",
    )
