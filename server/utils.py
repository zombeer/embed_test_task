from exceptions import not_authorized_exception, user_not_found_exception
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models import User
from passlib.context import CryptContext

SECRET_KEY = "some_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Auth helper. Gets instance of current User using token payload or raise corresponding exception.
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


def authenticate_user(username: str, password: str) -> User | None:
    """
    Returns User instance of username/password pair is correct. Otherwise rises corresponding Exceptions.
    """
    user = User.get_or_none(User.name == username)
    if not user:
        raise user_not_found_exception
    if not verify_password(password, user.password):
        raise not_authorized_exception
    return user


def decode_jwt(token: str) -> dict:
    """
    Decodes JWT to dict.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if password matches hashed version.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Produces hashed version of password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict):
    """
    Creates JWT token out of payload dictionary.
    """
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
