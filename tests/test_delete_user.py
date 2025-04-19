import json
import pytest
from unittest.mock import patch
from user_handlers import delete_user

mock_user = {
    "email": "denis@example.com",
    "name": "Denis",
    "password": "secret",
    "last_login": None
}

def event_with_body(body):
    return {"body": json.dumps(body)}

@patch("user_handlers.delete_user.user_repo")
def test_delete_user_success(mock_repo):
    mock_repo.get_user_by_email.return_value = mock_user.copy()
    mock_repo.delete_user.return_value = 200
    event = {"pathParameters": {"email": mock_user["email"]}}

    response = delete_user.lambda_handler(event, None)

    assert response["statusCode"] == 204

@patch("user_handlers.delete_user.user_repo")
def test_delete_user_not_found(mock_repo):
    mock_repo.get_user_by_email.return_value = None
    event = {"pathParameters": {"email": mock_user["email"]}}

    response = delete_user.lambda_handler(event, None)

    assert response["statusCode"] == 404

@patch("user_handlers.delete_user.user_repo")
def test_delete_user_missing_path(mock_repo):
    mock_repo.get_user_by_email.return_value = None
    event = {} # Just blank 

    response = delete_user.lambda_handler(event, None)

    assert response["statusCode"] == 400
    assert "Missing path parameter: email" in response["body"]