import json
import boto3
import requests
import os
import time
import uuid

dynamodb = boto3.client('dynamodb')
ipstack_api_key = 'b8e2c14e0acb362f9bbc3edf011fe928'

def handler(event, context):
    print('Received event: ')
    print(event)

    user_id = str(uuid.uuid4())
    print(f'Logging visit for user {user_id}')
    ip = event['ip']
    
    # Get location data from IPStack API
    ipstack_url = f'http://api.ipstack.com/{ip}?access_key={ipstack_api_key}'
    response = requests.get(ipstack_url)
    location = response.json()
    print('Location data: ')
    print(location)

    # Store visit data in DynamoDB
    table_name = os.environ['VISITS_TABLE']
    dynamodb.put_item(
        TableName=table_name,
        Item={
            'userId': {'S': user_id},
            'visitTimestamp': {'S': time.strftime('%Y-%m-%d %H:%M:%S')},
            'visitTimestampEST': {'S': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time() - 5*3600))},
            "ip": {'S': ip},
            "type": {'S': location.get('type')},
            "continent_code": {'S': location.get('continent_code')},
            "continent_name": {'S': location.get('continent_name')},
            "country_code": {'S': location.get('country_code')},
            "country_name": {'S': location.get('country_name')},
            "region_code": {'S': location.get('region_code')},
            "region_name": {'S': location.get('region_name')},
            "city": {'S': location.get('city')},
            "zip": {'S': location.get('zip')},
            "latitude": {'S': str(location.get('latitude'))},
            "longitude": {'S': str(location.get('longitude'))},
            'full_json': {'S': json.dumps(location)},
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Logged visit with location')
    }