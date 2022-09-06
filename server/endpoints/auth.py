from exceptions import user_exists_exception
from fastapi import APIRouter
from models.utils import add_user
from schemas.inbound import LoginPayload
from schemas.outbound import Token
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
    response_model=Token,
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
    return Token(access_token=access_token, token_type="bearer")
