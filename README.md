# simple-user-service-exercise

This repo deploys a very simple user REST api using AWS API Gateway, AWS Lambda, and AWS DynamoDB 

Resources are creted using the SAM template template.yaml

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
