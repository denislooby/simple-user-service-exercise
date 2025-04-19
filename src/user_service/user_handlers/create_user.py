import json

from pydantic import ValidationError
from user_persistence import user_repo
from user_models import UserCreate

def lambda_handler(event, context):
    try:
        user = UserCreate.model_validate_json(event["body"])
    except ValidationError as e:
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid input", "errors": e.errors()})}
    email = user.email
    
    if user_repo.get_user_by_email(email): # Can't add same email twice as we key off it.
        return {"statusCode": 400, "body": json.dumps({"message": "User with this email already exists."})}

    user_object = {
        "email": email,
        "name": user.name,
        "password": user.password,
        "last_login": None
    }

    user_repo.save_user(user_object)
    return {"statusCode": 200, "body": json.dumps(user_object)}