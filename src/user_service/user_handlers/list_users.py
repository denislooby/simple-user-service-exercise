import json
from user_persistence import user_repo

def lambda_handler(event, context):
    try:
        users = user_repo.list_users()
        return {"statusCode": 200, "body": json.dumps(users)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": "Error listing users", "errors": e.errors})}
    
    
