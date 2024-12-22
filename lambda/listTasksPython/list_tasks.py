import boto3
import os

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ.get('TABLE_NAME')
    table = dynamodb.Table(table_name)

    # Scan table to retrieve all tasks
    try:
        response = table.scan()
        tasks = response.get('Items', [])
        return {
            "statusCode": 200,
            "body": {
                "message": "Tasks retrieved successfully",
                "tasks": tasks
            }
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": {
                "message": "Failed to retrieve tasks",
                "error": str(e)
            }
        }