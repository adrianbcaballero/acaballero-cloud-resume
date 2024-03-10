import json
import time
import urllib.parse
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
sns = boto3.client('sns')
sns_topic_arn = "${sns_topic_arn}"

def lambda_handler(event, context):
    key = event['Records'][0]['s3']['object']['key']
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    website_bucket = "www.adriancaballeroresume.com"

    source = {'Bucket': source_bucket, 'Key': key}
    
    try:
        response = s3.meta.client.copy(source, website_bucket, key)
        logger.info("File copied to the destination bucket successfully!")

        #publish message to SNS 
        message = f"Updated website content"
        sns.publish(TopicArn=sns_topic_arn, Message=message, Subject="Updated Website contents")
    
    except Exception as e:
        # Log error message
        logger.error("Not run")

        raise e
