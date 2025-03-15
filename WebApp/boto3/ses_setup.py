import boto3

ses_client = boto3.client("ses", region_name="us-east-1")

SENDER_EMAIL = "your-email@example.com"
RECIPIENT_EMAIL = "recipient@example.com"

# Verify sender email (Run this once)
ses_client.verify_email_identity(EmailAddress=SENDER_EMAIL)
print(f"✅ Sender Email Verified: {SENDER_EMAIL}")

# Send test email
response = ses_client.send_email(
    Source=SENDER_EMAIL,
    Destination={"ToAddresses": [RECIPIENT_EMAIL]},
    Message={
        "Subject": {"Data": "AWS Deployment Notification"},
        "Body": {"Text": {"Data": "This is a test email from AWS SES."}},
    },
)

print(f"✅ Test Email Sent to {RECIPIENT_EMAIL}")
