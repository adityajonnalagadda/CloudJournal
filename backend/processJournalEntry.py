import json
import boto3
import os
import re 
from datetime import datetime, timedelta


comprehend = boto3.client('comprehend')
dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns') 

TABLE_NAME = os.environ.get('TABLE_NAME', 'journal-entries')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '') 


HARM_KEYWORDS = r'\b(kill myself|suicide|self harm|hopeless|want to die|ending it all)\b'
ALERT_PHONE_NUMBER = "+91 8220745557"

def lambda_handler(event, context):
   
    try:
        body = json.loads(event['body'])
        entry_text = body['entryText']
        user_id = body.get('userId', 'demo-user')    


        response = dynamodb.query(
            TableName=TABLE_NAME,
            KeyConditionExpression='userId = :uid',
            ExpressionAttributeValues={':uid': {'S': user_id}},
            ScanIndexForward=False, 
            Limit=1 
        )
       
        if 'Items' in response and len(response['Items']) > 0:
 
            last_timestamp = response['Items'][0]['timestamp']['S']
  
            last_date = datetime.fromisoformat(last_timestamp.replace('Z', ''))
   
            new_date = last_date + timedelta(days=1)
        else:

            new_date = datetime(2025, 9, 1, 10, 0, 0) 
       
 
        timestamp = new_date.isoformat() + "Z"

        sentiment_response = comprehend.detect_sentiment(
            Text=entry_text,
            LanguageCode='en'
        )
        sentiment = sentiment_response['Sentiment']


        if re.search(HARM_KEYWORDS, entry_text, re.IGNORECASE):

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=f'CRITICAL SENTIMENT ALERT - CALL {ALERT_PHONE_NUMBER}',
                Message=(
                    f"A critical alert was triggered by a journal entry.\n\n"
                    f"URGENT: Please follow up by calling {ALERT_PHONE_NUMBER}.\n\n"
                    f"User: {user_id}\n"
                    f"Time: {timestamp}\n"
                    f"Entry Text: {entry_text}\n"
                )
            )

            sentiment = "CRITICAL"


        item = {
            'userId': {'S': user_id},
            'timestamp': {'S': timestamp},
            'text': {'S': entry_text},
            'sentiment': {'S': sentiment}
        }


        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item=item
        )


        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'message': 'Entry saved successfully!', 'timestamp': timestamp})
        }

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'error': str(e)})
        }