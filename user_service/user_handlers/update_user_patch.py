import json
from user_persistence import user_repo

def lambda_handler(event, context):
    email = event["pathParameters"]["email"]
    body = json.loads(event["body"])

    # Check the user exists first 
    if not user_repo.get_user_by_email(email):
        return {"statusCode": 404, "body": "User not found"}

    user_repo.update_user(email, body)
    return {"statusCode": 204}