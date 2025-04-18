#!/bin/bash

# Set Python path to include user_service so imports work for tests
export PYTHONPATH=./user_service

echo "Running tests with PYTHONPATH=$PYTHONPATH"
pytest tests
