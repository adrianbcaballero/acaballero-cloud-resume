import json
import urllib.parse
import boto3

s3 = boto3.client('s3')
sns = boto3.client('sns')
sns_topic_arn = "${sns_topic_arn}"


def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    try:
        message = f"Updated website content"
        sns.publish(TopicArn=sns_topic_arn, Message=message, Subject="Updated Website contents")
        
    except Exception as e:
        print(e)
        print(f'Error handling S3 object. Make sure they exist and your bucket is in the same region as this function.')
        raise e
              