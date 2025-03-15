import boto3
import json

# AWS Clients
lambda_client = boto3.client("lambda", region_name="us-east-1")
iam_client = boto3.client("iam")
s3_client = boto3.client("s3")

# Configuration
LAMBDA_FUNCTION_NAME = "db_backup_lambda"
IAM_ROLE_NAME = "LambdaS3BackupRole"
S3_BUCKET_NAME = "my-db-backups-bucket"     # Provide your bucket name
LAMBDA_ZIP_FILE = "lambda_function.zip"
RDS_INSTANCE_ID = "my-rds-instance"         # Provide your DB instance id 
BACKUP_FILE_NAME = "db_backup"

# Step 1: Create an S3 Bucket for Backup
try:
    s3_client.create_bucket(Bucket=S3_BUCKET_NAME)
    print(f"✅ S3 Bucket Created: {S3_BUCKET_NAME}")
except s3_client.exceptions.BucketAlreadyOwnedByYou:
    print(f"⚠️ Bucket '{S3_BUCKET_NAME}' already exists.")

# Step 2: Create IAM Role for Lambda
assume_role_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}

role_response = iam_client.create_role(
    RoleName=IAM_ROLE_NAME,
    AssumeRolePolicyDocument=json.dumps(assume_role_policy)
)
role_arn = role_response["Role"]["Arn"]
print(f"✅ IAM Role Created: {IAM_ROLE_NAME}")

# Attach S3 and RDS permissions to the IAM Role
iam_client.attach_role_policy(
    RoleName=IAM_ROLE_NAME,
    PolicyArn="arn:aws:iam::aws:policy/AmazonS3FullAccess"
)
iam_client.attach_role_policy(
    RoleName=IAM_ROLE_NAME,
    PolicyArn="arn:aws:iam::aws:policy/AmazonRDSFullAccess"
)
print(f"✅ IAM Policies Attached to Role: {IAM_ROLE_NAME}")

# Step 3: Create the Lambda Function
with open(LAMBDA_ZIP_FILE, "rb") as f:
    zip_content = f.read()

lambda_response = lambda_client.create_function(
    FunctionName=LAMBDA_FUNCTION_NAME,
    Runtime="python3.8",
    Role=role_arn,
    Handler="lambda_function.lambda_handler",
    Code={"ZipFile": zip_content},
    Timeout=60,
    MemorySize=128
)
print(f"✅ Lambda Function Created: {LAMBDA_FUNCTION_NAME}")
