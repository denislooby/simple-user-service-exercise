import json
from user_persistence import user_repo

def lambda_handler(event, context):

    email = event["pathParameters"]["email"]

    # Check the user exists first as delete in dynamodb is always success
    if not user_repo.get_user_by_email(email):
        return {"statusCode": 404, "body": "User not found"}

    # Delete and check status in case of some failure
    status_code = user_repo.delete_user(email)
    if status_code >= 400:
        return {
            "statusCode": status_code,
            "body": f"Failed to delete user: status {status_code}"
        }

    return {"statusCode": 204} # Ok no content 