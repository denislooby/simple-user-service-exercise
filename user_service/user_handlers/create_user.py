import json
from user_persistence import user_repo

def lambda_handler(event, context):
    body = json.loads(event["body"])
    email = body["email"]
    
    if user_repo.get_user_by_email(email): # Can't add same email twice as we key off it.
        return {"statusCode": 400, "body": json.dumps({"message": "User with this email already exists."})}

    user_object = {
        "email": email,
        "name": body["name"],
        "password": body["password"],
        "last_login": None
    }

    user_repo.save_user(user_object)
    return {"statusCode": 200, "body": json.dumps(user_object)}