from exceptions import user_not_found_exception
from fastapi import APIRouter, Depends
from models import User, post_filter_query_builder
from schemas import NewPostPayload, PostFilterPayload, PostSchema
from server.utils import get_current_user

router = APIRouter(
    tags=["Posts"],
)


@router.post(
    "/user/me/posts",
    name="Create new post by current user",
    response_model=PostSchema,
)
async def new_post(
    payload: NewPostPayload,
    current_user: User = Depends(get_current_user),
) -> PostSchema:
    """
    Creates a new post by current User.
    """
    new_post = current_user.add_post(**payload.dict())
    return PostSchema.from_orm(new_post)


@router.get(
    "/user/me/posts",
    name="Posts of the current User",
    response_model=list[PostSchema],
)
async def get_current_user_posts(
    q: PostFilterPayload = Depends(),
    current_user: User = Depends(get_current_user),
) -> list[PostSchema]:
    """
    List of current User posts.
    """
    result = []
    posts_query = post_filter_query_builder(current_user.posts, **q.dict())
    for post in list(posts_query):
        result.append(PostSchema.from_orm(post))
    return result


@router.get(
    "/user/{username}/posts",
    name="Posts of the target User",
    tags=["Posts"],
    response_model=list[PostSchema],
)
async def get_user_posts_by_username(
    username: str,
    q: PostFilterPayload = Depends(),
) -> list[PostSchema]:
    """
    List posts of the user with target username.
    """
    user = User.get_or_none(User.name == username).execute()
    if not user:
        raise user_not_found_exception
    result = []
    posts_query = post_filter_query_builder(user.posts, **q.dict())
    for post in list(posts_query):
        result.append(PostSchema.from_orm(post))
    return result
