import os
from datetime import datetime, timedelta

import boto3
from aws_lambda_powertools.utilities.parser import parse
from botocore.exceptions import ClientError

from app.src.create_image import ThumbnailAndPostCreator
from app.src.schemas.input_event_schema import CreatePostInputSchema

s3 = boto3.client('s3')


def lambda_handler(event, context):
    parsed_payload = parse(event=event, model=CreatePostInputSchema)

    post = ThumbnailAndPostCreator(parsed_payload.day_of_the_week, parsed_payload.date, parsed_payload.preacher, parsed_payload.theme)
    post.create_post()

    if post:

        # Upload the file to S3
        with open(os.path.abspath('./src/created-images/post.png'), 'rb') as file:
            # generate a unique key for the file
            key = f"files/{datetime.now().strftime('%Y%m%d-%H%M%S')}-post"
            
            # upload the file to S3
            try:
                s3.upload_fileobj(file, 'church-manager-bucket', key)
            except ClientError as e:
                print(e)
                return {
                    'statusCode': 500,
                    'body': 'Error uploading file to S3'
                }
            
            # generate a pre-signed URL that expires in two minutes
            url_expiration = datetime.now() + timedelta(minutes=2)
            url = s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': 'church-manager-bucket',
                    'Key': key
                },
                ExpiresIn=url_expiration
            )

            return { "statusCode": "200", "message": "Image creation succeded", "url": url}
    else:
        return { "statusCode": "500", "message": "Image creaton failed"}