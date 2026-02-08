import json
import boto3
import os

dynamodb = boto3.client('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME', 'journal-entries')

def lambda_handler(event, context):
    try:
        # Getting query parameters from the API Gateway event
        params = event.get('queryStringParameters', {})
        user_id = params.get('userId', 'demo-user')

        response = dynamodb.query(
            TableName=TABLE_NAME,
            # Query for all items where the partition key 'userId' = :uid
            KeyConditionExpression='userId = :uid',
            ExpressionAttributeValues={
                ':uid': {'S': user_id}
            },
            # Sorting from newest to oldest
            ScanIndexForward=False 
        )

        # Formatting the DynamoDB items into a clean JSON list
        items = []
        for item in response.get('Items', []):
            items.append({
                'timestamp': item['timestamp']['S'],
                'text': item['text']['S'],
                'sentiment': item['sentiment']['S']
            })

        # Returning the list of items
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps(items)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps({'error': str(e)})
        }
