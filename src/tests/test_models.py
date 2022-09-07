import pytest
from config import DB_URI
from models import User
from models.utils import add_user

TEST_USER_1 = "TestUser1"
TEST_USER_2 = "TestUser2"


@pytest.fixture(autouse=True, scope="session")
def check_db_name():
    if "test" not in DB_URI.lower():
        pytest.exit(
            reason='You must run tests against test DB provided via DB_URI env var(should contain "test" substring in name)'
        )


def test_add_user():
    user = add_user(username=TEST_USER_1, password="password")
    assert user.name == TEST_USER_1, f"Created user name should be a {TEST_USER_1}"
    assert user.bio == "", "Created user name should be empty"
    assert user.subscriptions == [], "Created user subscriptions should be empty"
    assert user.subscriptions_count == 0, "Created user subscriptions count should be 0"


def test_add_user_second_time():
    add_user(username=TEST_USER_1, password="password")
    user = add_user(username=TEST_USER_1, password="password")
    assert user is None, "Should return None if User already exists"


def test_get_user():
    user = add_user(username=TEST_USER_1, password="password")
    user = User.get_by_id(TEST_USER_1)
    assert user.name == TEST_USER_1, "Should get proper user by username"


def test_user_subscribe():
    user1 = User.get_by_id(TEST_USER_1)
    user2 = add_user(username=TEST_USER_2, password="password")

    user1.add_subscription(user2)
    assert user1.subscriptions_count == 1, "Should be 1 after subscribing"
    assert user2.subscribers_count == 1, "Should be 1 after subscribing"
    assert user1.subscriptions == [
        TEST_USER_2
    ], "Should have proper list of subscriptions"


def test_user_add_post():
    user1 = User.get_by_id(TEST_USER_1)
    user2 = User.get_by_id(TEST_USER_2)

    post = user2.add_post("title", "text")
    assert (
        post.title == "title" and post.text == "text"
    ), "Should return proper post instance"

    assert user2.posts.count() == 1, "Posts count should be 1 "
    assert (
        user1.feed().count() == 1
    ), "User1 feed should be of leghth 1 after User2 adds post"
