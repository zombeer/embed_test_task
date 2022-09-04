from http.client import HTTPException

from fastapi import status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
)

user_exists_exception = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Username already exists"
)
