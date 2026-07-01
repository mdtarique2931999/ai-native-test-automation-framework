import pytest
import requests
from jsonschema import validate

JSONPLACEHOLDER = "https://jsonplaceholder.typicode.com"
HTTPBIN = "https://httpbin.org"

POST_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title", "body"],
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
}


@pytest.mark.api
def test_auth_token_validation():
    """httpbin bearer endpoint validates token-based auth behavior."""
    token = "testmu-sdet1-token"
    response = requests.get(
        f"{HTTPBIN}/bearer",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["authenticated"] is True
    assert body["token"] == token


@pytest.mark.api
def test_crud_operations():
    create_response = requests.post(
        f"{JSONPLACEHOLDER}/posts",
        json={"title": "test", "body": "body", "userId": 1},
        timeout=15,
    )
    assert create_response.status_code == 201

    read_response = requests.get(f"{JSONPLACEHOLDER}/posts/1", timeout=15)
    assert read_response.status_code == 200

    update_response = requests.put(
        f"{JSONPLACEHOLDER}/posts/1",
        json={"id": 1, "title": "updated", "body": "updated", "userId": 1},
        timeout=15,
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "updated"

    delete_response = requests.delete(f"{JSONPLACEHOLDER}/posts/1", timeout=15)
    assert delete_response.status_code == 200


@pytest.mark.api
def test_error_handling_404():
    response = requests.get(f"{JSONPLACEHOLDER}/posts/999999", timeout=15)
    assert response.status_code == 404


@pytest.mark.api
def test_error_handling_4xx_and_5xx():
    bad_request = requests.post(f"{HTTPBIN}/status/400", timeout=15)
    assert bad_request.status_code == 400

    server_error = requests.get(f"{HTTPBIN}/status/500", timeout=15)
    assert server_error.status_code == 500


@pytest.mark.api
def test_schema_validation():
    response = requests.get(f"{JSONPLACEHOLDER}/posts/1", timeout=15)
    assert response.status_code == 200
    validate(instance=response.json(), schema=POST_SCHEMA)


@pytest.mark.api
def test_rate_limiting_simulation():
    response = requests.get(f"{HTTPBIN}/status/429", timeout=15)
    assert response.status_code == 429
