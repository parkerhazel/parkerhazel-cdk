import json
import boto3
import requests
import os

dynamodb = boto3.client('dynamodb')
ipstack_api_key = 'YOUR_API_KEY'

def handler(event, context):
    body = json.loads(event['body'])
    user_id = body['userId']
    ip = body['ip']
    
    # Get location data from IPStack API
    ipstack_url = f'http://api.ipstack.com/{ip}?access_key={ipstack_api_key}'
    response = requests.get(ipstack_url)
    location = response.json()

    # Store visit data in DynamoDB
    table_name = os.environ['VISITS_TABLE']
    dynamodb.put_item(
        TableName=table_name,
        Item={
            'userId': {'S': user_id},
            'visitTimestamp': {'S': str(time.time())},
            'location': {'S': json.dumps(location)},
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Logged visit with location')
    }