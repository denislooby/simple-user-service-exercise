import json
import pytest
from unittest.mock import patch
from user_handlers import login_user

mock_user = {
    "email": "denis@example.com",
    "name": "Denis",
    "password": "secret",
    "last_login": None
}

def event_with_body(body):
    return {"body": json.dumps(body)}

@patch("user_handlers.login_user.user_repo")
def test_login_success(mock_repo):
    mock_repo.get_user_by_email.return_value = mock_user.copy()
    event = event_with_body({"email": "denis@example.com", "password": "secret"})

    response = login_user.lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["email"] == "denis@example.com"
    assert "last_login" in body

@patch("user_handlers.login_user.user_repo")
def test_login_wrong_password(mock_repo):
    mock_repo.get_user_by_email.return_value = mock_user.copy()
    event = event_with_body({"email": "denis@example.com", "password": "wrong"})

    response = login_user.lambda_handler(event, None)

    assert response["statusCode"] == 401
