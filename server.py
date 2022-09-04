from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from auth import authenticate_user, create_access_token, decode_jwt, get_password_hash
from exceptions import (
    not_authorized_exception,
    user_exists_exception,
    user_not_found_exception,
)
from models import User, create_tables, create_user
from schemas import (
    Post,
    Token,
    UpdateUserProfilePayload,
    UserPasswordPayload,
    UserProfile,
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
    Get instance of current User using token payload
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


@app.post("/signup", response_model=Token)
async def signup(
    payload: UserPasswordPayload,
) -> Token:
    """
    Create new User by selecting a username and password.
    """
    payload.password = get_password_hash(payload.password)
    user = create_user(**payload.dict())
    if not user:
        raise user_exists_exception

    access_token = create_access_token(data={"sub": user.name})
    return Token(access_token=access_token, token_type="bearer")


@app.post("/token", response_model=Token)
async def login_for_access_token(
    payload: UserPasswordPayload,
) -> Token:
    """
    User login via username/password pair.
    """
    user = authenticate_user(payload.username, payload.password)
    access_token = create_access_token(data={"sub": user.name})
    return Token(access_token=access_token, token_type="bearer")


@app.get("/user", response_model=UserProfile)
async def get_user(current_user: User = Depends(get_current_user)) -> UserProfile:
    return UserProfile.from_orm(current_user)


@app.put("/user", response_model=UserProfile)
async def update_user(
    payload: UpdateUserProfilePayload,
    current_user: User = Depends(get_current_user),
) -> User:
    payload_dict = payload.dict(exclude_none=True)
    current_user.update(**payload_dict).execute()
    return User.get_by_id(current_user.name)


@app.get("/user/{user_id}", **user_model_output)
async def user_by_id(user_id: int):
    return User(id=user_id, name=f"User_{user_id}")


@app.get(
    "/users",
    response_model=list[UserProfile],
)
async def get_users_list() -> list[UserProfile]:
    return [UserProfile(name="Vasya"), UserProfile(name="Volodya", password="ololo")]


@app.get(
    "/user/posts",
    response_model=Post,
)
async def get_user_posts(current_user: User = Depends(get_current_user)) -> list[Post]:
    return []
