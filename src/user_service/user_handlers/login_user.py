"""
Lambda function for the POST /login endpoint.

Validates the email and password provided match those in the DB
"""
import json
from datetime import datetime, timezone

from pydantic import ValidationError
from user_persistence import user_repo
from user_models import LoginRequest

def lambda_handler(event, context):
    """
    Handle user login request.

    Validates the incoming request body, checks if email and password match DB.

    Args:
        event (dict): AWS Lambda event object. Expects JSON 'body' with user email and password.
        context (LambdaContext): AWS Lambda context (unused).

    Returns:
        dict: Response with statusCode and body.
    """
    try:
        user = LoginRequest.model_validate_json(event["body"])
    except ValidationError as e:
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid input", "errors": e.errors()})}
    email = user.email
    password = user.password

    user = user_repo.get_user_by_email(email, consistent_read=True)
    if not user or user.get("password") != password:
        return {"statusCode": 401, "body": json.dumps({"message": "Invalid email or password"}) }

    # Set last login time
    user["last_login"] = datetime.now(tz=timezone.utc).isoformat()
    user_repo.update_user(email, {"last_login": user["last_login"]})


    return {"statusCode": 200, "body": json.dumps(user)}
