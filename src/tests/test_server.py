from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_read_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_user():
    response = client.post(
        "/signup", json={"username": "TestUser", "password": "testPassword123!@#"}
    )
    assert response.status_code == 200
    assert (
        "access_token" in response.json().keys()
    ), "Successful signup response should contain token"
    assert (
        "token_type" in response.json().keys()
    ), "Successful signup response should contain token type"


def test_random_token():
    response = client.get("/user/me", headers={"Authorizaition": "Bearer any"})
    assert response.status_code == 401, "Should return 401 Unauthorized"
