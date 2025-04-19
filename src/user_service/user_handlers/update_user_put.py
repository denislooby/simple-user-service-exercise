"""
Lambda function for the PUT /user endpoint.

Updates an existing user in DynamoDB after validating input.
"""
import json

from pydantic import ValidationError
from user_persistence import user_repo
from user_models import UserUpdatePut

def lambda_handler(event, context):
    """
    Handle user update request.

    Validates the incoming request body and updates the user in DynamoDB.
    This one is for the PATCH endpoint so allows partial objects in the body

    Args:
        event (dict): AWS Lambda event object. Expects 'body' with updated user JSON and pathParameters with email.
        context (LambdaContext): AWS Lambda context (unused).

    Returns:
        dict: Response with statusCode and body.
    """
    if not event.get("pathParameters") or not event["pathParameters"].get("email"):
        return {"statusCode": 400, "body": json.dumps({"message": "Missing path parameter: email"}) }
    
    email = event["pathParameters"].get("email")
    try:
        user = UserUpdatePut.model_validate_json(event["body"])
    except ValidationError as e:
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid input", "errors": e.errors()})}

    if not user_repo.get_user_by_email(email): # Not allowing PUT to create
        return {"statusCode": 404, "body": json.dumps({"message": "User not found"})}

    user_repo.update_user(email, user.model_dump())
    return {"statusCode": 204}