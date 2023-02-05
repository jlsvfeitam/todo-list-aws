#!/bin/bash

source todo-list-aws/bin/activate
set -x
mkdir .aws
touch .aws/credentials
echo "[default]" > .aws/credentials
echo "aws_access_key_id = AKIAUNBGN4AV3CGB6WGZ" >> .aws/credentials
echo "aws_secret_access_key = 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" >> .aws/credentials
echo "aws_session_token =" >> .aws/credentials
chmod 600 .aws/credentials
sam validate --region us-east-1
sam build
