import boto3

sns_client = boto3.client("sns", region_name="us-east-1")

# Slack/MS Teams Webhook URL (Replace with actual webhook URL)
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXX/YYY/ZZZ"

# Load SNS topic ARNs
with open("sns_topic_arns.txt") as f:
    topic_arns = {line.split(":")[0]: line.split(":")[1].strip() for line in f}

# Subscribe the webhook to SNS topics
for topic_name, topic_arn in topic_arns.items():
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol="https",
        Endpoint=SLACK_WEBHOOK_URL,
    )
    print(f"✅ Subscribed {topic_name} to {SLACK_WEBHOOK_URL}")
