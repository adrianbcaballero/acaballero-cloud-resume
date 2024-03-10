import json
import urllib.parse
import boto3

s3 = boto3.client('s3')
sns = boto3.client('sns')
sns_topic_arn = "${sns_topic_arn}"


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    website_bucket = 'www.adriancaballeroresume.com'
    
    try:
        #move s3 branch content to website s3
        copy_source = {
            'Bucket': bucket,
            'Key': key
        }
        bucket = s3.Bucket(website_bucket)
        bucket.copy(copy_source, key)

        #publish message to SNS 
        message = f"Updated website content"
        sns.publish(TopicArn=sns_topic_arn, Message=message, Subject="Updated Website contents")
    except Exception as e:
        print(e)
        print(f'Error in websitesyncing')
        raise e
              