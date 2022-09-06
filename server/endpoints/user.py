from fastapi import APIRouter, Depends, Path
from models import User
from schemas import UpdateUserProfilePayload, UserProfile
from server.utils import get_current_user

router = APIRouter(
    tags=["User profile"],
)


@router.get(
    "/user/me",
    response_model=UserProfile,
    name="Get current User profile data.",
)
async def get_user(current_user: User = Depends(get_current_user)) -> UserProfile:
    """
    Gets current User profile data.
    """
    return UserProfile.from_orm(current_user)


@router.put(
    "/user/me",
    response_model=UserProfile,
    name="Update current User profile data",
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


@router.get(
    "/user/{username}",
    response_model=UserProfile,
    name="Get User profile by username",
)
async def user_by_username(username: str = Path(..., title="Username of target User.")):
    """
    Gets current User profile data.
    """
    user = User.get_by_id(username)
    return UserProfile.from_orm(user)
