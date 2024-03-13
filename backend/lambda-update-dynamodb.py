import boto3
import logging
import os
import json

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
        http_response = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({
                'message': 'Value updated successfully',
                'value': new_viewcount
            })
        }
        
        return http_response
    except Exception as e:
        logger.error("An error occurred: %s", str(e))
        # Return an error response
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }
