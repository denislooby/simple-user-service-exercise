import boto3
import os

local_run = os.getenv("AWS_SAM_LOCAL")
dynamodb = None
table = None

def get_table():
    # Need to defer creating dynamodb and table to function 
    # or unit tests try to init it on import
    global table, dynamodb
    if table:
        return table

    region = os.getenv("AWS_REGION", "eu-west-1")

    if local_run:
        print("Using local dynomo db")
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://host.docker.internal:8000") 
    else:
        print("Using local cloud db")
        dynamodb = boto3.resource("dynamodb") 

    # Make table name changeable for testing other branches on AWS
    table = dynamodb.Table(os.environ.get("USER_TABLE", "UserTable")) 
    return table

def get_user_by_email(email: str,  consistent_read: bool = False):
    """
    Get user object by email

    Args:
        email (str) The users email address

    Returns:
        The user object
    """
    table = get_table()
    response = table.get_item(Key={"email": email}, ConsistentRead=consistent_read)
    return response.get("Item")

def save_user(user_item: dict):
    """
    Save the provided user object dict to the DB
    Args:
        user_item (dict) The dict to save
    Returns:
        None
    """
    table = get_table()
    table.put_item(Item=user_item)

def update_user(email: str, updates: dict):
    """
    Update a user record in the DB
    Args:
        email (str) The email of the user
        update (dict) The updated fields
    Returns:
        None
    """
    table = get_table()
    # 'name' was causing issues with dynamodb so need to use expressionAttributeNames
    update_expression = "SET " + ", ".join(f"#{k} = :{k}" for k in updates) 
    expression_attribute_names = {f"#{k}": k for k in updates}
    expression_attribute_values = {f":{k}": v for k, v in updates.items()}

    table.update_item(
        Key={"email": email},
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values
    )

def delete_user(email: str):
    """
    Delete a user from the DB
    Args:
        email (str) The email of the user to be deleted
    Returns:
        HTTP Status code 
    """
    table = get_table()
    response = table.delete_item(Key={"email": email})
    return response['ResponseMetadata']['HTTPStatusCode']

def list_users():
    """
    Get a List of all users from the DB
    Args:
        None
    Returns:
        List of users objects

    """
    table = get_table()
    response = table.scan() # Gets everything but only upto 1Mb at a time so need loop
    users = response['Items']
    while response.get('LastEvaluatedKey'):
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        users.extend(response['Items'])
    return users