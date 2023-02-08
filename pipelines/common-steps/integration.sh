#!/bin/bash

source todo-list-aws/bin/activate
set -x
export BASE_URL=$1
#For translate
python -m pip install awscli
aws --version
pytest -s test/integration/todoApiTest.py