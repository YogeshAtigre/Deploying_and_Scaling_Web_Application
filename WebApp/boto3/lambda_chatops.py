import boto3
import os
import json

sns_client = boto3.client("sns", region_name="us-east-1")

# Load SNS topic ARNs
SNS_TOPIC_SUCCESS = os.getenv("SNS_TOPIC_SUCCESS")
SNS_TOPIC_FAILURE = os.getenv("SNS_TOPIC_FAILURE")

def lambda_handler(event, context):
    deployment_status = event.get("status")
    message = event.get("message", "No details provided.")
    
    # Determine the SNS topic
    if deployment_status == "success":
        topic_arn = SNS_TOPIC_SUCCESS
        subject = "🚀 Deployment Succeeded!"
    else:
        topic_arn = SNS_TOPIC_FAILURE
        subject = "❌ Deployment Failed!"
    
    # Publish message to SNS
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps(event),
        Subject=subject,
    )
    
    print(f"✅ Notification Sent: {subject}")
    return response
