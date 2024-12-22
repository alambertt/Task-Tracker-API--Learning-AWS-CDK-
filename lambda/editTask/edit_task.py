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
    
    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Invalid JSON in request body"
            })
        }
    
    if not task_id:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Missing taskId parameter"
            })
        }
    
    # Remove any empty or None values from the update
    update_attrs = {k: v for k, v in body.items() if v}
    if not update_attrs:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "No valid attributes to update"
            })
        }
    
    # Construct update expression and attribute values
    update_expression = "SET " + ", ".join(f"#{k} = :{k}" for k in update_attrs.keys())
    expression_attribute_names = {f"#{k}": k for k in update_attrs.keys()}
    expression_attribute_values = {f":{k}": v for k, v in update_attrs.items()}
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    
    try:
        response = table.update_item(
            Key={'taskId': task_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='ALL_NEW'
        )
        
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
                "message": f"Task {task_id} updated successfully",
                "task": response['Attributes']
            })
        }
        
    except ClientError as e:
        logger.error(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Failed to update task",
                "error": str(e)
            })
        }
