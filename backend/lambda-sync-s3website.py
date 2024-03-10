import json
import urllib.parse
import boto3

s3 = boto3.client('s3')
sns = boto3.client('sns')
sns_topic_arn = "${sns_topic_arn}"


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

        #publish message to SNS 
        message = f"Updated website content"
        sns.publish(TopicArn=sns_topic_arn, Message=message, Subject="Updated Website contents")
    except Exception as e:
        print(e)
        print(f'Error in website syncing')
        raise e
              