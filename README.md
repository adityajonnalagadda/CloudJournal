# MoodLog – Cloud-Based Journal & Sentiment Analysis App

MoodLog is a serverless web application that allows users to log daily journal entries, analyze emotional trends using AWS NLP services, and receive alerts for critical mental health patterns.

This project demonstrates a full-stack cloud architecture using **HTML/CSS/JavaScript + AWS Lambda + API Gateway + DynamoDB + Amazon Comprehend + SNS**.

---

## What This Project Does

### Journal Logging
Users can write daily journal entries through a web interface.  
Each entry is sent to a backend API and stored in DynamoDB.

---

### Sentiment Analysis (AI)
Every journal entry is analyzed using **Amazon Comprehend**, which classifies the text into:
- POSITIVE  
- NEGATIVE  
- NEUTRAL  
- MIXED  
- CRITICAL  

---

### Emotional Trend Analysis
Users can request summaries for:
- Today  
- This week  
- This month  
- Last 6 months  

The backend aggregates sentiment data and returns insights and encouragement messages.

---

### Journal History Viewer
Users can fetch all past journal entries sorted by timestamp.

---

### Mental Health Alerts
The system detects harmful keywords (e.g., self-harm phrases).  
If detected, it triggers an **Amazon SNS alert notification**.

---

Setup Backend on AWS (Lambda + API Gateway)
## Step 1: Create DynamoDB Table

Table Name: journal-entries

Partition Key: userId (String)

Sort Key: timestamp (String)

## Step 2: Create Lambda Functions

Create 3 Lambda functions:

Function Name	File
processJournalEntry	processJournalEntry.py
getJournalHistory	getJournalHistory.py
getAnalysis	getAnalysis.py

Set environment variables:

TABLE_NAME = journal-entries
SNS_TOPIC_ARN = your_sns_topic_arn

## Step 3: Enable Amazon Comprehend

No configuration needed—Lambda uses AWS SDK.

## Step 4: Setup API Gateway

Import the provided OpenAPI file:
JournalAPI-prod-oas30-apigateway.yaml
Deploy the API and note the Invoke URL.

## Step 5: Connect Frontend to API

Edit app.js and replace:
const API_URL = "YOUR_API_GATEWAY_URL";

## Step 6: Setup SNS Alerts 

Create SNS Topic
Subscribe email or SMS
Add topic ARN to Lambda environment variables

# Technologies Used

HTML5,
CSS3,
JavaScript, 
Backend,
Python (AWS Lambda),
Amazon API Gateway,
Amazon DynamoDB,
Amazon Comprehend,
Amazon SNS,
