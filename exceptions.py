"""
Custom exceptions for the aplication
"""
from fastapi import HTTPException, status

# Exception to handle auth errors
not_authorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
)

# Exeption to handle duplicate username error
user_exists_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
)

# Exception to handle user not found error
user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
)

# Exeption to handle duplicate subscription error
subscription_exists_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Subscription already exists"
)

# Exception to handle user not found error
subscription_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found"
)
