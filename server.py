from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError

from auth import authenticate_user, create_access_token, decode_jwt
from exceptions import credentials_exception, user_exists_exception
from schemas import Post, Token, User

fake_users_db = {}


app = FastAPI(
    title="Embed test API",
    description="Some basic user-post CRUD API example...",
    contact={"email": "zombeer@gmail.com"},
    version="0.1.0",
    servers=[{"url": "https://localhost"}],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

user_model_output = {
    "response_model": User,
    "response_model_exclude_none": True,
    "response_model_exclude": ["password"],
}


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:

    try:
        payload = decode_jwt(token)
        username = payload.get("sub")
        if username is None:
            raise
    except JWTError:
        raise credentials_exception
    # user = get_user(fake_users_db, username=username)
    user = User(name=username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/signup", response_model=Token)
async def signup(username: str, password: str) -> Token:
    # create user
    user = User(name=username, password=password)
    access_token = create_access_token(data={"sub": user.name})
    return Token(access_token=access_token, token_type="bearer")


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise credentials_exception
    access_token = create_access_token(data={"sub": user.name})
    return Token(access_token=access_token, token_type="bearer")


@app.get("/user", **user_model_output)
async def get_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@app.put("/user", **user_model_output)
async def update_user(
    updated_data: User, current_user: User = Depends(get_current_user)
) -> User:
    return updated_data


@app.get("/user/{user_id}", **user_model_output)
async def user_by_id(user_id: int):
    return User(id=user_id, name=f"User_{user_id}")


@app.get(
    "/users",
    response_model=list[User],
    response_model_exclude_none=True,
    response_model_exclude=["password"],
)
async def get_users_list() -> list[User]:
    return [User(name="Vasya"), User(name="Volodya", password="ololo")]


@app.get(
    "/user/posts",
    response_model=Post,
)
async def get_user_posts(current_user: User = Depends(get_current_user)) -> list[Post]:
    return []
