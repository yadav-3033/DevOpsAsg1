# import json


# def hello(event, context):
#     body = {
#         "message": "Hi, Abhinav Yadav this side."
#     }

#     return {"statusCode": 200, "body": json.dumps(body)}


import json
import boto3
from uuid import uuid4
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DevOpsAsg1-table')

def create_todo(event, context):
    data = json.loads(event['body'])
    todo_id = str(uuid4())
    item = {
        'id': todo_id,
        'task': data['task'],
        'completed': False
    }
    table.put_item(Item=item)
    response = {
        'statusCode': 201,
        'body': json.dumps(item)
    }
    return response

def get_todo(event, context):
    todo_id = event['pathParameters']['id']
    result = table.get_item(Key={'id': todo_id})
    if 'Item' in result:
        response = {
            'statusCode': 200,
            'body': json.dumps(result['Item'])
        }
    else:
        response = {
            'statusCode': 404,
            'body': json.dumps({'error': 'TODO item not found'})
        }
    return response

def update_todo(event, context):
    todo_id = event['pathParameters']['id']
    data = json.loads(event['body'])
    result = table.update_item(
        Key={'id': todo_id},
        UpdateExpression="set task=:t, completed=:c",
        ExpressionAttributeValues={
            ':t': data['task'],
            ':c': data['completed']
        },
        ReturnValues="UPDATED_NEW"
    )
    response = {
        'statusCode': 200,
        'body': json.dumps(result['Attributes'])
    }
    return response

def delete_todo(event, context):
    todo_id = event['pathParameters']['id']
    table.delete_item(Key={'id': todo_id})
    response = {
        'statusCode': 204
    }
    return response
