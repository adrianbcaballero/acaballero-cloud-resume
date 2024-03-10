import json
import time
import urllib.parse
import boto3
import os

s3 = boto3.client('s3')
sns = boto3.client('sns')
sns_topic_arn = "${sns_topic_arn}"
s3_sync_website = os.environ.get('s3_sync_website')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    website_bucket = 'www.adriancaballeroresume.com'
    
    try:
        # Get a list of all objects in the source bucket
        source_bucket = s3.Bucket(bucket)
        for obj in source_bucket.objects.all():
            # Copy each object to the destination bucket
            copy_source = {
                'Bucket': bucket,
                'Key': obj.key
            }
            s3.meta.client.copy(copy_source, website_bucket, obj.key)
        
        print("Website syncing completed successfully")

        #publish message to SNS 
        message = f"Updated website content"
        sns.publish(TopicArn=sns_topic_arn, Message=message, Subject="Updated Website contents")

        #basic logs if successful
        cloudwatch_logs.put_log_events(logGroupName=s3_sync_website, logEvents=[{'timestamp': int(round(time.time() * 1000))}])
    
    except Exception as e:
        # Log error message
        print(f"Error in website syncing: {str(e)}")

        # Log the error
        if s3_sync_website:
            cloudwatch_logs = boto3.client('logs')
            log_message = f"Error in website syncing: {str(e)}"
            cloudwatch_logs.create_log_group(logGroupName=s3_sync_website)
            cloudwatch_logs.put_log_events(logGroupName=s3_sync_website, logEvents=[{'message': log_message, 'timestamp': int(round(time.time() * 1000))}])
        
        raise e
              