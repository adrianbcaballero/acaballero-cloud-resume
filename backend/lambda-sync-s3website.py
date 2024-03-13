import json
import os
import boto3

s3 = boto3.client('s3')
sns = boto3.client('sns')
cloudfront = boto3.client('cloudfront')

def lambda_handler(event, context):
    try:
        # Delete objects in www.adriancaballeroresume.com
        website_bucket_name = 'www.adriancaballeroresume.com'
        prefix = ''
        response = s3.list_objects_v2(Bucket=website_bucket_name, Prefix=prefix)
        if 'Contents' in response:
            for obj in response['Contents']:
                print('Deleting', obj['Key'])
                s3.delete_object(Bucket=website_bucket_name, Key=obj['Key'])
        
        # Copying contents from branch content s3 to website s3
        src_bucket_name = 'adriancaballero-branchcontent'
        dest_bucket_name = 'www.adriancaballeroresume.com'

        # Iterate over all objects in the source bucket
        response = s3.list_objects_v2(Bucket=src_bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                copy_source = {'Bucket': src_bucket_name, 'Key': obj['Key']}
                s3.copy_object(CopySource=copy_source, Bucket=dest_bucket_name, Key=obj['Key'])
                print(obj['Key'] + ' - File Copied')

        # Send SNS of website updating
        sns_topic_arn = os.environ['SNS_TOPIC_ARN']
        message = "New front end files were uploaded and Website content will be updated"
        sns.publish(TopicArn=sns_topic_arn, Message=message, Subject="Updated Website contents")

        #invalidate cloudfront cache
        distribution_id = 'EZZ8DJS18WL3N'
        cloudfront.create_invalidation(
            DistributionID = distribution_id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': 1,
                    'Items': ['/*'] 
                },
                'CallerReference': 's3-bucket-change-invalidation'  
            }
        )
        
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
