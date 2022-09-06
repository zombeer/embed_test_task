# import pytest
from fastapi.testclient import TestClient
from models import Post, Subscription, User
from peewee import SqliteDatabase
from server import app

# models = [User, Post, Subscription]


# @pytest.fixture
# def db():
#     yield SqliteDatabase(":memory:")

db = SqliteDatabase(":memory:")
tables = [User, Post, Subscription]

client = TestClient(app)


def setup_function():
    db.bind(tables)
    db.create_tables(tables)


def teardown_function():
    db.drop_tables(tables)
    db.close()


def test_read_main():
    response = client.get("/")
    assert response.status_code == 404


def test_read_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # assert response.json() == []


def test_add_user():
    response = client.post(
        "/signup", json={"username": "TestUser", "password": "testPassword"}
    )
    assert response.status_code == 422
