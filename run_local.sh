#!/bin/bash

# Script for local SAM + DynamoDB Local testing
# Starts DynamoDB container and creates table
# If passed stop arg stops container and unsets env

if [ "$1" == "stop" ]; then
    if docker ps | grep -q dynamodb-local; then
        echo "Stopping DynamoDB Local container..."
        docker stop dynamodb-local
        docker rm dynamodb-local
    fi

if [[ "$AWS_ACCESS_KEY_ID" == "dummy" ]]; then
    unset AWS_ACCESS_KEY_ID
    unset AWS_SECRET_ACCESS_KEY
    unset AWS_SESSION_TOKEN
    echo "Dummy AWS creds cleared"
else
    echo "Leaving AWS creds alone"
fi

  echo "Unsetting local environment variables..."
  unset DYNAMODB_ENDPOINT
  echo "Local environment cleaned up."
  return
fi

if [[ -z "$AWS_ACCESS_KEY_ID" || "$AWS_ACCESS_KEY_ID" == "dummy" ]]; then
    export AWS_ACCESS_KEY_ID=dummy
    export AWS_SECRET_ACCESS_KEY=dummy
    echo "Using dummy AWS credentials for local DynamoDB"
else
    echo "Real AWS credentials detected — leaving alone"
fi

# Start dynamodb Local (if not already running)
if ! docker ps | grep -q dynamodb-local; then
  echo "Starting DynamoDB Local container..."
  docker run -d --name dynamodb-local -p 8000:8000 amazon/dynamodb-local
  export DYNAMODB_ENDPOINT=http://localhost:8000

    echo "Waiting for DynamoDB Local to start..."
    for i in {1..10}; do
    if curl -s http://localhost:8000 > /dev/null; then
        echo "DynamoDB Local is ready."
        break
    fi
    sleep 1
    done

  echo "Creating UserTable"
  aws dynamodb create-table \
    --table-name UserTable \
    --attribute-definitions AttributeName=email,AttributeType=S \
    --key-schema AttributeName=email,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --endpoint-url $DYNAMODB_ENDPOINT \
    --region eu-west-1 
else
  echo "DynamoDB Local is already running."
fi

export DYNAMODB_ENDPOINT=http://localhost:8000 # Set again in case docker was running
echo "Environment set for local testing:"
echo "  DYNAMODB_ENDPOINT=$DYNAMODB_ENDPOINT"

echo "You can now run:"
echo "  sam local invoke CreateUserFunction --event events/create_user.json " 
echo "  sam local invoke LoginUserFunction --event events/login_user.json    etc"  
echo "  run ./run_local stop to clean up " 