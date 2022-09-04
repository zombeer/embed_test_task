from fastapi import HTTPException, status

not_authorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
)

user_exists_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
)


user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
)
