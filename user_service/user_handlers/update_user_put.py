import json
from user_persistence import user_repo

def lambda_handler(event, context):
    email = event["pathParameters"].get("email")
    body = json.loads(event["body"])

    if not user_repo.get_user_by_email(email): # Not allowing PUT to create
        return {"statusCode": 404, "body": "User not found"}

    # Ensure all required fields are present
    # PUT should update the entire object
    required_fields = ["name", "password", "last_login"]
    missing = [field for field in required_fields if field not in body]
    if missing:
        return {
            "statusCode": 400,
            "body": f"Missing required fields: {', '.join(missing)}"
        }

    user_repo.update_user(email, body)
    return {"statusCode": 204}