import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client('dynamodb')
table = dynamodb.Table('Website-access')

def lambda_handler(event, context):
    try:
        response = dynamodb.update_item(
            Key={"website_id": {"S": "adriancaballeroresume.com"}},
            UpdateExpression="set access_count = if_not_exists(access_count, :start) + :increase",
            ExpressionAttributeValues={":start": {"N": "0"}, ":increase": {"N": "1"}},
            ReturnValues="UPDATED_NEW",
            )

        logger.info("Response: %s", response)
    except Exception as e:
        logger.error("An error occurred: %s", str(e))