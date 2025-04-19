"""
Lambda function for the PATCH /user endpoint.

Updates an existing user in DynamoDB after validating input.
"""
import json

from pydantic import ValidationError
from user_persistence import user_repo
from user_models import UserUpdatePatch

def lambda_handler(event, context):
    """
    Handle user update request.

    Validates the incoming request body and updates the user in DynamoDB.
    This one is for the PUT endpoint so expects the whole object minus the key(email)

    Args:
        event (dict): AWS Lambda event object. Expects 'body' with updated user JSON and pathParameters with email.
        context (LambdaContext): AWS Lambda context (unused).

    Returns:
        dict: Response with statusCode and body.
    """
    if not event.get("pathParameters") or not event["pathParameters"].get("email"):
        return {"statusCode": 400, "body": json.dumps({"message": "Missing path parameter: email"})}
    
    email = event["pathParameters"]["email"]
    try:
        user = UserUpdatePatch.model_validate_json(event["body"])
    except ValidationError as e:
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid input", "errors": e.errors()})}
    

    # Check the user exists first 
    if not user_repo.get_user_by_email(email):
        return {"statusCode": 404, "body": json.dumps({"message": "User not found"})}

    user_repo.update_user(email, user.model_dump())
    return {"statusCode": 204}