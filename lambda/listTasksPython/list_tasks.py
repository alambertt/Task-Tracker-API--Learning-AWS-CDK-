import boto3
import os
import logging
import json

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ.get('TABLE_NAME')
    logger.info(f"TABLE_NAME: {table_name}")
    
    try:
        table = dynamodb.Table(table_name)
        response = table.scan()
        logger.info(f"Scan Response: {response}")
        
        tasks = response.get('Items', [])
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Tasks retrieved successfully",
                "tasks": tasks
            })
        }
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Failed to retrieve tasks",
                "error": str(e)
            })
        }