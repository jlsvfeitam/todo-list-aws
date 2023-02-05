#!/bin/bash

source todo-list-aws/bin/activate
set -x
mkdir ${HOME}/.aws
chmod 775 ${HOME}/.aws
touch ${HOME}/.aws/credentials
echo "[default]" > ${HOME}/.aws/credentials
echo "aws_access_key_id = AKIAUNBGN4AV3CGB6WGZ" >> ${HOME}/.aws/credentials
echo "aws_secret_access_key = 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" >> ${HOME}/.aws/credentials
echo "aws_session_token =" >> ${HOME}/.aws/credentials
chmod 600 ${HOME}/.aws/credentials
sam validate --region us-east-1
sam build
