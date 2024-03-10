import json
import time
import urllib.parse
import boto3
import os
import logging

logger = logging.getLogger()
s3 = boto3.client('s3')
sns = boto3.client('sns')
sns_topic_arn = "${sns_topic_arn}"
s3_sync_website = os.environ.get('websites3_sync_lambda')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    website_bucket = 'www.adriancaballeroresume.com'
    
    try:
        # Get a list of all objects in the source bucket
        response = s3.list_objects_v2(Bucket=bucket)
        if 'Contents' in response:
            for obj in response['Contents']:
                # Copy each object to the destination bucket
                copy_source = {
                    'Bucket': bucket,
                    'Key': obj['Key']
                }
                s3.copy_object(CopySource=copy_source, Bucket=website_bucket, Key=obj['Key'])
        
        print("Website syncing completed successfully")

        #publish message to SNS 
        message = f"Updated website content"
        sns.publish(TopicArn=sns_topic_arn, Message=message, Subject="Updated Website contents")

        
        logger.info("function started")
    
    except Exception as e:
        # Log error message
        logger.error("Not run")

        raise e
