from exceptions import subscription_exists_exception
from fastapi import APIRouter, Depends
from models import IntegrityError, User
from models.utils import post_filter_query_builder
from schemas.inbound import PostFilterPayload, Username
from schemas.outbound import MessageSchema, PostSchema, PostWithAuthorSchema
from server.utils import get_current_user

router = APIRouter(
    tags=["Subscriptions"],
)


@router.get(
    "/user/me/subscriptions",
    name="Posts of current user subscripte",
    response_model=list[PostWithAuthorSchema],
)
async def get_current_user_subscriptions(
    q: PostFilterPayload = Depends(),
    current_user: User = Depends(get_current_user),
) -> list[PostWithAuthorSchema]:
    """
    Lists posts by current user subscriptions.
    It was quite complicated to write proper docstring to this function (:
    """
    result = []
    posts_query = post_filter_query_builder(current_user.feed(), **q.dict())

    for post in posts_query:
        result.append(PostWithAuthorSchema(**post.as_dict()))
    return result


@router.post(
    "/user/me/subscriptions",
    name="Add subscription",
    response_model=MessageSchema,
)
async def subscribe(
    payload: Username,
    current_user: User = Depends(get_current_user),
) -> list[PostWithAuthorSchema]:
    """
    Adds provided username to current user subscriptions.
    """
    import ipdb

    ipdb.set_trace()
    try:
        current_user.add_subscription(payload.username)
    except IntegrityError:
        raise subscription_exists_exception
    return MessageSchema(detail="Subscription added succeessfully")


@router.delete(
    "/user/me/subscriptions",
    name="Delete subscription",
    response_model=MessageSchema,
)
async def delete_subscription(
    payload: Username,
    current_user: User = Depends(get_current_user),
) -> list[PostSchema]:
    """
    Deletes provided username from current user subscriptions.
    """
    # User.delete_subscription() can raise subscription_not_found_exception by itself. In order to handle exceprions properly I would add two levels of custom exceptions:
    # Model level and server level to isolate models dependencies from server package. Keeping this one as it is just for saving time.
    current_user.delete_subscription(payload.username)
    return MessageSchema(detail="Subscription removed succeessfully")
