import json
import os
import boto3

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    sns_topic_arn = os.environ['SNS_TOPIC_ARN']
    try:
        message = "New front end files were uploaded and Website content will be updated"
        sns.publish(TopicArn=sns_topic_arn, Message=message, Subject="Updated Website contents")
        
    except Exception as e:
        print("Error publishing message to SNS topic:", e)
        raise e
              