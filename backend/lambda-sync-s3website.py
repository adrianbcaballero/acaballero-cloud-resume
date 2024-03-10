import json
import boto3

def lambda_handler(event, context):
    source_bucket_name = 'adriancaballero-branchcontent'
    destination_bucket_name = 'www.adriancaballeroresume.com'
    s3 = boto3.client('s3')

    try:
        response = s3.list_objects_v2(Bucket=source_bucket_name)
        for obj in response.get('Contents', []):
            # Get the key of the object
            key = obj['Key']

            # Copy the object from source to destination bucket
            copy_source = {
                'Bucket': source_bucket_name,
                'Key': key
            }
            destination_key = key  # You can change the destination key if needed
            s3.copy_object(CopySource=copy_source, Bucket=destination_bucket_name, Key=destination_key)

        # Return success message
        return {
            'statusCode': 200,
            'body': json.dumps('Files copied successfully!')
        }

    except Exception as e:
        # Log error message
        print("An error occurred:", str(e))
        raise e

