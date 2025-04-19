import json

from pydantic import ValidationError
from user_persistence import user_repo
from user_models import UserUpdatePatch

def lambda_handler(event, context):
    if not event.get("pathParameters") or not event["pathParameters"].get("email"):
        return {"statusCode": 400, "body": "Missing path parameter: email"}
    
    email = event["pathParameters"]["email"]
    try:
        user = UserUpdatePatch.model_validate_json(event["body"])
    except ValidationError as e:
        return { "statusCode": 400, "body": f"Invalid input: {e.errors()}" }

    # Check the user exists first 
    if not user_repo.get_user_by_email(email):
        return {"statusCode": 404, "body": "User not found"}

    user_repo.update_user(email, user.model_dump())
    return {"statusCode": 204}