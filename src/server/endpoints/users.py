from fastapi import APIRouter
from models import Post, User
from models.utils import get_top_users
from schemas.outbound import UserProfileWithPosts

router = APIRouter(tags=["List users"])


@router.get(
    "/users",
    response_model=list[UserProfileWithPosts],
    name="List all user profiles with their 5 latest posts.",
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


@router.get(
    "/users/top",
    response_model=list[UserProfileWithPosts],
    name="List top user profiles with their 5 latest posts.",
)
async def get_top20_profiles() -> list[UserProfileWithPosts]:
    """
    List top20 users with their recent posts.
    """
    result = []
    for u in get_top_users():
        u.posts = list(u.posts.order_by(Post.id.desc()).limit(5))
        profileWithPosts = UserProfileWithPosts.from_orm(u)
        result.append(profileWithPosts)
    return result
