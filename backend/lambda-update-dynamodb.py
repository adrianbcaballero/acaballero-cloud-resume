import boto3
import logging
import os
import json
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Use boto3.resource instead of boto3.client
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        # Get the HTTP method from the event
        http_method = event.get('httpMethod', 'POST')
        logger.info("HTTP Method: %s", http_method)
        
        # Access the DynamoDB table
        table = dynamodb.Table('Website-access')
        
        # Handle GET request - return current count WITHOUT incrementing
        if http_method == 'GET':
            logger.info("GET request - fetching current count without incrementing")
            
            # Get the current item
            response = table.get_item(
                Key={"website_id": "adriancaballeroresume.com"}
            )
            
            # Extract the current count (default to 0 if item doesn't exist)
            if 'Item' in response:
                current_count = int(response['Item'].get('access_count', 0))
            else:
                current_count = 0
            
            logger.info("Current count (not incremented): %s", current_count)
            
            return {
                'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                'body': json.dumps({
                    'message': 'Current count retrieved successfully',
                    'value': current_count
                })
            }
        
        # Handle POST request - increment the counter
        elif http_method == 'POST':
            logger.info("POST request - incrementing count")
            
            response = table.update_item(
                Key={"website_id": "adriancaballeroresume.com"},
                UpdateExpression="set access_count = if_not_exists(access_count, :start) + :increase",
                ExpressionAttributeValues={":start": 0, ":increase": 1},
                ReturnValues="UPDATED_NEW",
            )
            logger.info("Response: %s", response)
            
            # Retrieve the updated access count
            new_viewcount = response['Attributes']['access_count']
            # Convert Decimal to int
            new_viewcount = int(new_viewcount)
            
            logger.info("New count after increment: %s", new_viewcount)
            
            return {
                'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                'body': json.dumps({
                    'message': 'Value updated successfully',
                    'value': new_viewcount
                })
            }
        
        # Handle OPTIONS request (for CORS preflight)
        elif http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                'body': json.dumps({'message': 'CORS preflight successful'})
            }
        
        # Handle unsupported methods
        else:
            logger.warning("Unsupported HTTP method: %s", http_method)
            return {
                'statusCode': 405,
                'headers': {
                    "Access-Control-Allow-Origin": "*"
                },
                'body': json.dumps({'error': 'Method Not Allowed'})
            }
    
    except Exception as e:
        logger.error("An error occurred: %s", str(e))
        # Return an error response
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps({'error': 'Internal Server Error', 'details': str(e)})
        }