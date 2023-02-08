#!/bin/bash

source todo-list-aws/bin/activate
set -x
export BASE_URL=$1
#For translate
aws --version
pytest -s test/integration/todoApiTest.py