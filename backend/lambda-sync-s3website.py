import json
import os
import boto3

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    try:
        #delete objects in www.adriancaballeroresume.com
        website_bucket_name = 'www.adriancaballeroresume.com'
        prefix = ''
        response = s3_client.list_objects_v2(Bucket=website_bucket_name, Prefix=prefix)
        for object in response['Contents', []]:
            print('Deleting', object['Key'])
            s3_client.delete_object(Bucket=website_bucket_name, Key=object['Key'])
        
        #send sns of website updating
        sns_topic_arn = os.environ['SNS_TOPIC_ARN']
        message = "New front end files were uploaded and Website content will be updated"
        sns.publish(TopicArn=sns_topic_arn, Message=message, Subject="Updated Website contents")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Website content updated and SNS sent successfully')
        }
    except Exception as e:
        print("An error occurred:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('Error occurred while updating website content')
        }
              