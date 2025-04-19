import json
from user_persistence import user_repo

def lambda_handler(event, context):
    """
    Handle user delete request.

    Checks if users exists and deletes if it does

    Args:
        event (dict): AWS Lambda event object. Expects 'pathPArameters' with user email.
        context (LambdaContext): AWS Lambda context (unused).

    Returns:
        dict: Response with statusCode.
    """
    if not event.get("pathParameters") or not event["pathParameters"].get("email"):
        return {"statusCode": 400, "body": json.dumps({"message": "Missing path parameter: email"})}
    
    email = event["pathParameters"]["email"]

    # Check the user exists first as delete in dynamodb is always success
    if not user_repo.get_user_by_email(email):
        return {"statusCode": 404, "body": json.dumps({"message": "User not found"})}
    

    # Delete and check status in case of some failure
    status_code = user_repo.delete_user(email)
    if status_code >= 400:
        return {
            "statusCode": status_code,
            "body": json.dumps({"message": f"Failed to delete user: status {status_code}"}) 
        }

    return {"statusCode": 204} # Ok no content 