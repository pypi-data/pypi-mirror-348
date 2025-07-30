from fastapi import status
from fastapi.testclient import TestClient


def test_access_token_not_authenticated(client: TestClient) -> None:
    response = client.post(
        "/auth/token", data={"username": "notfound", "password": "123"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
