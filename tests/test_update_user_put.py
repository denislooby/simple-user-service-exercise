import json
import pytest
from unittest.mock import patch
from user_handlers import update_user_put

mock_user = {
    "name": "Denis",
    "password": "secret",
    "last_login": None
}

def event_with_body(body):
    return {"body": json.dumps(body)}


def event_with_path_and_body(path_params, body):
    return {"body": json.dumps(body), "pathParameters": path_params}


@patch("user_handlers.update_user_put.user_repo")
def test_update_user_success(mock_repo):
    mock_repo.get_user_by_email.return_value = mock_user.copy()
    mock_repo.update_user.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    updated = mock_user.copy()
    updated["name"] = "Updated"
    event = event_with_path_and_body({"email": "denis@example.com"}, updated)

    response = update_user_put.lambda_handler(event, None)
    assert response["statusCode"] == 204

@patch("user_handlers.update_user_put.user_repo")
def test_update_user_missing(mock_repo):
    mock_repo.get_user_by_email.return_value = None
    event = event_with_path_and_body({"email": "denis@example.com"}, mock_user)

    response = update_user_put.lambda_handler(event, None)

    assert response["statusCode"] == 404

@patch("user_handlers.update_user_put.user_repo")
def test_update_user_obj_incomplete(mock_repo):
    mock_repo.get_user_by_email.return_value = mock_user.copy()
    event = event_with_path_and_body({"email": "denis@example.com"}, {"password": "password", "name": "Denis"})

    response = update_user_put.lambda_handler(event, None)

    assert response["statusCode"] == 400
    assert "Field required" in response["body"]

@patch("user_handlers.update_user_put.user_repo")
def test_update_user_missing_path(mock_repo):
    mock_repo.get_user_by_email.return_value = None
    user = mock_user.copy()
    event = event_with_body(user)

    response = update_user_put.lambda_handler(event, None)

    assert response["statusCode"] == 400
    assert "Missing path parameter: email" in response["body"]


@patch("user_handlers.update_user_put.user_repo")
def test_update_user_extra_field(mock_repo):
    mock_repo.get_user_by_email.return_value = None
    user = mock_user.copy()
    user['extraFiled'] = "Not allowed"
    event = event_with_path_and_body({"email": "denis@example.com"}, user)

    response = update_user_put.lambda_handler(event, None)

    assert response["statusCode"] == 400
    assert "Extra inputs are not permitted" in response["body"]