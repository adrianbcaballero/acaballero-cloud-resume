import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Use boto3.resource instead of boto3.client
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        # Access the DynamoDB table using the resource's Table method
        table = dynamodb.Table('Website-access')

        response = table.update_item(
            Key={"website_id": "adriancaballeroresume.com"},
            UpdateExpression="set access_count = if_not_exists(access_count, :start) + :increase",
            ExpressionAttributeValues={":start": 0, ":increase": 1},
            ReturnValues="UPDATED_NEW",
        )
        logger.info("Response: %s", response)
        
        #return new value to api
        new_viewcount = response['Atrributes']['access_count']
        return{
            'statusCode': 200,
            'body': {
                'message': 'Value updated successfully',
                'value': new_viewcount
            }
        }
    except Exception as e:
        logger.error("An error occurred: %s", str(e))
