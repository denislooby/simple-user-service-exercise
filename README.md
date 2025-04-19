# simple-user-service-exercise

This repo deploys a very simple user REST api using AWS API Gateway, AWS Lambda, and AWS DynamoDB 
Pydantic is used to validate incoming data.

Resources are created using the SAM template template.yaml

## Deploying the  application

To build and deploy to AWS run the following:

```bash
sam build --use-container
sam deploy --guided
```

To test locally run the script run_local.sh first.
This will start a local DynamoDB container and create the required table.
run_local.sh stop will remove container and clean env

```bash
 source run_local.sh
 sam local invoke CreateUserFunction --event events/create_user.json
 source run_local stop
```

There is test event json for each endpoint in the events folder.

## Using the service

### Endpoints
#### Create User
* **POST** `/user` - Creates a new user
```bash
curl -X POST https://<api-id>.execute-api.eu-west-1.amazonaws.com/Prod/user \
  -H "Content-Type: application/json" \
  -d '{
        "email": "denis@example.com",
        "name": "Denis",
        "password": "secret123"
      }'
```

#### Update User
* **PUT** `/user/{email}` - Update full User resource
```bash
curl -X PUT https://<api-id>.execute-api.eu-west-1.amazonaws.com/Prod/user/denis%40example.com \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Denis Updated",
        "password": "newsecret",
        "last_login": null
      }''
```
* **PATCH** `/user/{email}` - Update partial User resource
```bash
curl -X PATCH https://<api-id>.execute-api.eu-west-1.amazonaws.com/Prod/user/denis%40example.com \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Denny"
      }'
```

#### Delete User
* **DELETE** `/user/{email}` - Delete a user
```bash
curl -X DELETE https://<api-id>.execute-api.eu-west-1.amazonaws.com/Prod/user/denis%40example.com
```

#### List Users
* **GET** `/users` - List all users
```bash
curl https://<api-id>.execute-api.eu-west-1.amazonaws.com/Prod/users
```

#### Login Endpoint
* **POST** `/login` - Validate users password against DB
```bash
curl -X POST https://<api-id>.execute-api.eu-west-1.amazonaws.com/Prod/login \
  -H "Content-Type: application/json" \
  -d '{
        "email": "denis@example.com",
        "password": "secret123"
      }'
```

## Limitations of the service
### Password storage and return from endpoints
Passwords are being stored as plaintext and also returned in the responses from some endpoints.
This is bad practice and passwords should never be stored. 
Instead bcrypt should be used to hash and salt the password and that is what should be stored.
The login endpoint would then compare hashes and no endpoint should return the password or hash in a response.
```python
  # Hashing of password to store in db
  hashed = bcrypt.hashpw("plaintext".encode(), bcrypt.gensalt())

  # Checking of hashed password in login
  bcrypt.checkpw("plaintext".encode(), hashed)
```
### Endpoint auth and access control.
There is not authentication on the endpoints.
A real service would need to restrict access.
Different levels of access would also be required with an admin type user having more access.
This could be implemented by adding a role element to the user object.
The login endpoint could return a JWT that encoded the user role.
The other endpoints could then require the JWT and use the role to enforce RBAC.
So an Admin could update and user, but a user could only update their own user object.

### Using the user email as primary key
The email is not ideal as the primary key for the user.
It gets used in the path elements for the user update and delete and will need to be urlencoded. 
The user can never change their email address but this may not be an issue.
A uuid could be used as a user id, login returns the user object so a user could use the id from there with PUT and PATCH.

### Cold startup delays 
One drawback of the use of AWS Lambda is the coldstart up time.
There is a noticable delay of a second or two as the endpoints start on first access.
Subsequent access is fast so this is a tradeoff for the scalability.
Warm instances could be used for extra cost.

## Alternative Imnplementations 
Another option for implemention would be a containerised python application using the FastAPI framework.
This would use the SQLAlchemy framework for DB access.
This would allow SQLite to be used for a small scale service and external PostgreSQL to scale more.
Scaling could be done on this type of service by using more containers and a load balancer.
So a deployment to kubernettes with many replicas possibly using an autoscaler.  
The DB would probably be the eventual bottleneck 
