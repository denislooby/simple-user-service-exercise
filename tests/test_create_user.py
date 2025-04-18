import json
import pytest
from unittest.mock import patch
from user_handlers import create_user

mock_user = {
    "email": "denis@example.com",
    "name": "Denis",
    "password": "secret",
    "last_login": None
}

def event_with_body(body):
    return {"body": json.dumps(body)}

@patch("user_handlers.create_user.user_repo")
def test_create_user_success(mock_repo):
    mock_repo.get_user_by_email.return_value = None
    event = event_with_body(mock_user)

    response = create_user.lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["email"] == "denis@example.com"

@patch("user_handlers.create_user.user_repo")
def test_create_user_duplicate(mock_repo):
    mock_repo.get_user_by_email.return_value = mock_user.copy()
    event = event_with_body(mock_user)

    response = create_user.lambda_handler(event, None)

    assert response["statusCode"] == 400
    assert "already exists" in response["body"]