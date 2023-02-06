#!/bin/bash

source todo-list-aws/bin/activate
set -x
mkdir ${HOME}/.aws
chmod 775 ${HOME}/.aws
touch ${HOME}/.aws/credentials
echo "[default]" > ${HOME}/.aws/credentials
echo "aws_access_key_id = ${AWS_ACCESS_KEY_ID}" >> ${HOME}/.aws/credentials
echo "aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}" >> ${HOME}/.aws/credentials
echo "aws_session_token =" >> ${HOME}/.aws/credentials
chmod 600 ${HOME}/.aws/credentials
sam validate --region us-east-1
sam build
