import boto3
import os
import json
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Event received: {json.dumps(event)}")
    
    # Get the taskId from path parameters
    task_id = event.get('pathParameters', {}).get('taskId')
    
    if not task_id:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Missing taskId parameter"
            })
        }
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    
    try:
        # Delete the item from DynamoDB
        response = table.delete_item(
            Key={'taskId': task_id},
            ReturnValues='ALL_OLD'  # This returns the deleted item
        )
        
        # Check if the item existed before deletion
        if 'Attributes' not in response:
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "message": f"Task with id {task_id} not found"
                })
            }
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": f"Task {task_id} deleted successfully",
                "deletedTask": response['Attributes']
            })
        }
        
    except ClientError as e:
        logger.error(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Failed to delete task",
                "error": str(e)
            })
        }
