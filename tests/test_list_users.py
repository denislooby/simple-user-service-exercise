import json
import pytest
from unittest.mock import patch
from user_handlers import list_users

mock_user = {
    "email": "denis@example.com",
    "name": "Denis",
    "password": "secret",
    "last_login": None
}

def event_with_body(body):
    return {"body": json.dumps(body)}

@patch("user_handlers.list_users.user_repo")
def test_list_users_success(mock_repo):
    mock_repo.list_users.return_value = [mock_user.copy()]
    event = {}

    response = list_users.lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert isinstance(body, list)
    assert body[0]["email"] == "denis@example.com"