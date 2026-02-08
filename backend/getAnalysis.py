import json
import boto3
import os
from datetime import datetime, timedelta

dynamodb = boto3.client('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME', 'journal-entries')

def lambda_handler(event, context):
    try:
        params = event.get('queryStringParameters', {})
        user_id = params.get('userId', 'demo-user')
        period = params.get('period', 'this-month')

        now = datetime.utcnow()
        if period == 'today':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'this-week':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == '6-months':
            start_date = now - timedelta(days=180)
        else: 
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
       
        start_timestamp = start_date.isoformat() + "Z"

        response = dynamodb.query(
            TableName=TABLE_NAME,
            KeyConditionExpression='userId = :uid AND #ts >= :start',
            ExpressionAttributeNames={
                '#ts': 'timestamp'
            },
            ExpressionAttributeValues={
                ':uid': {'S': user_id},
                ':start': {'S': start_timestamp}
            }
        )
       
        items = response.get('Items', [])
       
        entry_count = len(items)
        if entry_count == 0:
            summary = "No entries found for this period. Start writing to see your analysis!"
            trend = "NEUTRAL"
            encouragement = "Try to log your feelings today."
        else:
            
            sentiments = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0, 'MIXED': 0, 'CRITICAL': 0}
           
            for item in items:
                sentiment = item.get('sentiment', {}).get('S', 'NEUTRAL')
                if sentiment in sentiments:
                    sentiments[sentiment] += 1
                else:
                    
                    print(f"Unknown sentiment found: {sentiment}")
           

            if sentiments['CRITICAL'] > 0:
                trend = "Critical"
                encouragement = "Your analysis shows one or more critical entries. Please remember that help is available."
            elif sentiments['NEGATIVE'] > sentiments['POSITIVE']:
                trend = "Negative"
                encouragement = "It seems like a tough period. Remember that feelings are temporary. Be kind to yourself."
            elif sentiments['POSITIVE'] > sentiments['NEGATIVE']:
                trend = "Positive"
                encouragement = "You've had a positive outlook. Keep focusing on the good things!"
            else:
                trend = "Neutral"
                encouragement = "Your feelings seem balanced. Reflecting on this can be a great source of insight."


            summary = (
                f"You made {entry_count} entries this period.\n"
                f"• Critical: {sentiments['CRITICAL']}\n"
                f"• Negative: {sentiments['NEGATIVE']}\n"
                f"• Positive: {sentiments['POSITIVE']}\n"
                f"• Neutral: {sentiments['NEUTRAL']}\n"
                f"• Mixed: {sentiments['MIXED']}"
            )

        analysis = {
            'summary': summary,
            'trend': trend,
            'encouragement': encouragement
        }

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps(analysis)
        }
       
    except Exception as e:
        print(f"[ERROR] {str(e)}") 
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps({'error': 'Internal server error. Check Lambda logs.'})
        }