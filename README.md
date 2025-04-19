# simple-user-service-exercise

This repo deploys a very simple user REST api using AWS API Gateway, AWS Lambda, and AWS DynamoDB  
Pydantic is used to validate incoming data.  
AWS Resources are created using a SAM template.  

The service is for a user object that contains a name, email address, password and last login date.  
Endpoints are provided to Create, Update, Delete and List user objects.  
There is also a login endpoint to validate a provided email and password matches the stored one.  


## Deploying the  application
### Manual deploy to AWS
To build and deploy to AWS run the following:

```bash
sam build --use-container
sam deploy --guided
```

### Running locally with SAM local
To test locally run the script run_local.sh first.
This will start a local DynamoDB container and create the required table.
run_local.sh stop will remove container and clean env

```bash
 source run_local.sh
 sam local invoke CreateUserFunction --event events/create_user.json
 source run_local.sh stop
```

There is test event json for each endpoint in the events folder.

###  Deployment with GitHub Actions
Actions are provided to build and test with pytest.  
The [**Deploy to AWS**](https://github.com/denislooby/simple-user-service-exercise/actions/workflows/deploy.yaml) action will deploy the service to AWS.  
This can also be run against a branch, the branch name will be appended to the stack and table names.
To teardown the stack when finished use the action [**Teardown AWS Stack**](https://github.com/denislooby/simple-user-service-exercise/actions/workflows/teardown.yaml)

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
curl -X PUT https://<api-id>.execute-api.eu-west-1.amazonaws.com/Prod/user/denis@example.com \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Denis Updated",
        "password": "newsecret",
        "last_login": null
      }''
```
* **PATCH** `/user/{email}` - Update partial User resource
```bash
curl -X PATCH https://<api-id>.execute-api.eu-west-1.amazonaws.com/Prod/user/denis@example.com \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Denny"
      }'
```

#### Delete User
* **DELETE** `/user/{email}` - Delete a user
```bash
curl -X DELETE https://<api-id>.execute-api.eu-west-1.amazonaws.com/Prod/user/denis@example.com
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
There is no authentication on the endpoints.  
A real service would need to restrict access.  
Different levels of access would also be required with an admin type user having more access.  
This could be implemented by adding a role element to the user object.  
The login endpoint could return a JWT that encoded the user role.  
Like this.  
```python
    payload = {
        "sub": email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET-KEY, algorithm="HS256")
```
The other endpoints could then require the JWT and after decoding use the role to enforce RBAC.  
So an Admin could update any user, but a user could only update their own user object for example.  

### Using the user email as primary key
The email is not ideal as the primary key for the user.  
It gets used in the path elements and may have characters that need to be urlencoded.
The user can never change their email address but this may not be an issue.  
A uuid could be used as a user id, login returns the user object so a user could get the id from there to use with PUT and PATCH.  

### Cold startup delays 
One drawback of the use of AWS Lambda is the coldstart up time.  
There is a noticeable delay of a second or two as the endpoints start on first access.  
Subsequent access is fast so this is a tradeoff for the scalability.  
Warm instances could be used for extra cost.  

## Alternative Implementations 
Another option for implementation would be a containerised python application using the FastAPI framework.  
The SQLAlchemy library would be used for DB access.  
This would allow SQLite to be used for a small scale service and external PostgreSQL to scale more.  
Scaling could be done on this type of service by using more containers and a load balancer.  
So for example a deployment to kubernetes with many replicas possibly using an autoscaler.
The DB would probably become the bottleneck under heavy load.
