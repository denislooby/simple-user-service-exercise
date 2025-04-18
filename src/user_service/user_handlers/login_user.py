import json
from datetime import datetime, timezone
from user_persistence import user_repo

def lambda_handler(event, context):
    body = json.loads(event["body"])
    email = body["email"]
    password = body["password"]

    user = user_repo.get_user_by_email(email, consistent_read=True)
    if not user or user.get("password") != password:
        return {"statusCode": 401, "body": "Invalid email or password"}

    # Set last login time
    user["last_login"] = datetime.now(tz=timezone.utc).isoformat()
    user_repo.update_user(email, {"last_login": user["last_login"]})


    return {"statusCode": 200, "body": json.dumps(user)}
