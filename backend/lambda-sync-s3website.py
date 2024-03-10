import json
import time
import urllib.parse
import boto3
import os

s3 = boto3.client('s3')
sns = boto3.client('sns')
sns_topic_arn = "${sns_topic_arn}"
s3_sync_website = os.environ.get('websites3_sync_lambda')

#copies s3 branch content into website s3, sends sns, and logs with cloudwatch
def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    website_bucket = 'www.adriancaballeroresume.com'

    log_stream_name = context.aws_request_id
    
    # Initialize CloudWatch Logs client
    cloudwatch_logs = boto3.client('logs')
    
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

        # Put log events
        cloudwatch_logs.put_log_events(logGroupName=s3_sync_website, logStreamName=log_stream_name, logEvents=[{'timestamp': int(round(time.time() * 1000)), 'message': "Website syncing completed successfully"}])
    
    except Exception as e:
        # Log error message
        print(f"Error in website syncing: {str(e)}")

        # Log the error
        if s3_sync_website:
            log_message = f"Error in website syncing: {str(e)}"
            cloudwatch_logs.put_log_events(logGroupName=s3_sync_website, logStreamName=log_stream_name, logEvents=[{'timestamp': int(round(time.time() * 1000)), 'message': log_message}])
        
        raise e