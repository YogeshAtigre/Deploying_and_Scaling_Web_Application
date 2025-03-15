import boto3

sns_client = boto3.client("sns", region_name="us-east-1")

# Define SNS topics
TOPICS = {
    "DeploymentSuccess": "deployment-success-topic",
    "DeploymentFailure": "deployment-failure-topic",
}

topic_arns = {}

# Create SNS topics
for key, topic_name in TOPICS.items():
    response = sns_client.create_topic(Name=topic_name)
    topic_arns[key] = response["TopicArn"]
    print(f"✅ SNS Topic Created: {topic_name} ({response['TopicArn']})")

# Save ARNs for further use
with open("sns_topic_arns.txt", "w") as f:
    for key, arn in topic_arns.items():
        f.write(f"{key}: {arn}\n")
