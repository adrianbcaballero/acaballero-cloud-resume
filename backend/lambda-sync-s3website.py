import json
import time
import urllib.parse
import boto3
import os
import logging
import uuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client('sns')
sns_topic_arn = "${sns_topic_arn}"

response = s3.list_objects_v2(Bucket=source_bucket_name)

def lambda_handler(event, context):
    source_bucket_name = 'adriancaballero-branchcontent'
    destination_bucket_name = 'www.adriancaballeroresume.com'
    s3 = boto3.client('s3')


    try:
        response = s3.list_objects_v2(Bucket=source_bucket_name)
        for obj in response.get('Contents', []):
            # Get the key of the object
            key = obj['Key']

            # Copy the object from source to destination bucket
            copy_source = {
                'Bucket': source_bucket_name,
                'Key': key
            }
            destination_key = key  # You can change the destination key if needed
            s3.copy_object(CopySource=copy_source, Bucket=destination_bucket_name, Key=destination_key)

        # Return success message
        return {
            'statusCode': 200,
            'body': json.dumps('Files copied successfully!')
        }


        print(response)
        logger.info("File copied to the destination bucket successfully!")

        #publish message to SNS 
        message = f"Updated website content"
        sns.publish(TopicArn=sns_topic_arn, Message=message, Subject="Updated Website contents")
    
    except Exception as e:
        # Log error message
        logger.error("Not run")

        raise e
