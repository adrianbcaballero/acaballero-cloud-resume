import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        response = dynamodb.update_item(
        TableName = "Website-access"
        Key={"website_id": {"S": "hey"}},
        UpdateExpression="set access_count = if_not_exists(access_count, :start) + :increase",
        ExpressionAttributeValues={":start": {"N": "0"}, ":increase": {"N": "1"}},
        ReturnValues="UPDATED_NEW",
            )

        logger.info("Response: %s", response)
    except Exception as e:
        logger.error("An error occurred: %s", str(e))