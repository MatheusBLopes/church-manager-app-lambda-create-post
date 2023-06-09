#!/bin/bash

#
# variables
#

# AWS variables
AWS_REGION=us-east-1

PROJECT_NAME=LambdaCreatePost

LAMBDA_LAYER_NAME=second_python

# the directory containing the script file
dir="$(cd "$(dirname "$0")"; pwd)"
cd "$dir"

[[ $1 != 'prod' && $1 != 'dev' ]] && { echo 'usage: publish.sh <prod | dev>'; exit 1; } ;

# root account id
ACCOUNT_ID=$(aws sts get-caller-identity \
    --query Account \
    --output text)

echo aws lambda delete-alias $1
aws lambda delete-alias \
    --function-name $PROJECT_NAME \
    --name $1 \
    --region $AWS_REGION \
    2>/dev/null

echo zip lambda package
rm --force lambda.zip
chmod -R 777 ./app
zip -r lambda.zip app

echo aws lambda update-function-code $PROJECT_NAME
aws lambda update-function-code \
    --function-name $PROJECT_NAME \
    --zip-file fileb://lambda.zip \
    --region $AWS_REGION

echo zip layer package
pip install \
    --target=./python \
    --requirement ./app/requirements.txt
chmod -R 777 ./python
zip -r python.zip python

echo aws lambda publish-layer-version of $LAMBDA_LAYER_NAME
aws lambda publish-layer-version \
    --layer-name $LAMBDA_LAYER_NAME \
    --description "Updated version" \
    --zip-file fileb://python.zip

echo aws lambda update-function-code $PROJECT_NAME
VERSION=$(aws lambda publish-version \
    --function-name $PROJECT_NAME \
    --description $1 \
    --region $AWS_REGION \
    --query Version \
    --output text)
echo published version: $VERSION

echo get latest layer version
LATEST_LAYER_VERSION=$(aws lambda list-layer-versions \
    --layer-name $LAMBDA_LAYER_NAME \
    --query 'max_by(LayerVersions, &Version).Version')

echo $LATEST_LAYER_VERSION

echo update lambda $PROJECT_NAME layer version to $LATEST_LAYER_VERSION
aws lambda update-function-configuration \
    --function-name $PROJECT_NAME \
    --layers arn:aws:lambda:$AWS_REGION:$ACCOUNT_ID:layer:$LAMBDA_LAYER_NAME:$LATEST_LAYER_VERSION arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p39-pillow:1



echo aws lambda create-alias $1
aws lambda create-alias \
    --function-name $PROJECT_NAME \
    --name $1 \
    --function-version $VERSION \
    --region $AWS_REGION
