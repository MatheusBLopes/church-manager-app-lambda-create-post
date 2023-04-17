#!/bin/bash

#
# variables
#

# AWS variables
AWS_REGION=sa-east-1

PROJECT_NAME=LambdaCreateTask

LAMBDA_LAYER_NAME=basic_layer

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



echo zip layer package
mkdir basic-layer
pip install \
    --platform linux_x86_64 \
    --target=./basic-layer \
    --implementation cp \
    --python-version 3.9 \
    --only-binary=:all: \
    --requirement ./app/requirements.txt
chmod -R 777 ./basic-layer
cd basic-layer
zip -r basic-layer.zip .

echo aws lambda publish-layer-version of $LAMBDA_LAYER_NAME
aws lambda publish-layer-version \
    --layer-name $LAMBDA_LAYER_NAME \
    --description "Updated version" \
    --zip-file fileb://basic-layer.zip


echo aws lambda update-function-code $PROJECT_NAME
aws lambda update-function-code \
    --function-name $PROJECT_NAME \
    --zip-file fileb://lambda.zip \
    --region $AWS_REGION

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
    --layers arn:aws:lambda:$AWS_REGION:$ACCOUNT_ID:layer:$LAMBDA_LAYER_NAME:$LATEST_LAYER_VERSION
 
echo aws lambda create-alias $1
aws lambda create-alias \
    --function-name $PROJECT_NAME \
    --name $1 \
    --function-version $VERSION \
    --region $AWS_REGION
