from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "/docs" in response.url, "Root page must lead to /docs"


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


def test_add_post():
    response = client.post(
        "/token", json={"username": "TestUser", "password": "testPassword123!@#"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    new_post_payload = {"title": "Some new post title", "text": "Some new post text..."}
    response = client.post(
        "/user/me/posts",
        json=new_post_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, "Response code should be 200"
    assert "id" in response.json().keys(), "Reponse must contain 'id' field."
    assert "title" in response.json().keys(), "Reponse must contain 'title' field."
    assert "text" in response.json().keys(), "Reponse must contain 'text' field."
    assert "created" in response.json().keys(), "Reponse must contain 'created' field."


def test_random_token():
    response = client.get(
        "/user/me",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer any",
        },
    )
    assert response.status_code == 401, "Should return 401 Unauthorized"
