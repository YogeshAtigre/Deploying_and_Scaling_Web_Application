import boto3

# Initialize AWS Clients
ec2_client = boto3.client("ec2", region_name="us-east-1")
autoscaling_client = boto3.client("autoscaling", region_name="us-east-1")

# Step 1: Create VPC
vpc_response = ec2_client.create_vpc(CidrBlock="10.0.0.0/16")
vpc_id = vpc_response["Vpc"]["VpcId"]
ec2_client.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={"Value": True})
ec2_client.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={"Value": True})

print(f"✅ Created VPC: {vpc_id}")

# Step 2: Create Subnets
subnet_response = ec2_client.create_subnet(VpcId=vpc_id, CidrBlock="10.0.1.0/24")
subnet_id = subnet_response["Subnet"]["SubnetId"]
print(f"✅ Created Subnet: {subnet_id}")

# Step 3: Create Security Group
sg_response = ec2_client.create_security_group(
    GroupName="backend-sg",
    Description="Allow traffic for backend services",
    VpcId=vpc_id
)
sg_id = sg_response["GroupId"]

# Allow inbound traffic on ports 80, 443, and 5000 (for backend services)
ec2_client.authorize_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=[
        {"IpProtocol": "tcp", "FromPort": 80, "ToPort": 80, "IpRanges": [{"CidrIp": "0.0.0.0/0"}]},
        {"IpProtocol": "ssh", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "0.0.0.0/0"}]},
        {"IpProtocol": "tcp", "FromPort": 3000, "ToPort": 3000, "IpRanges": [{"CidrIp": "0.0.0.0/0"}]},
        {"IpProtocol": "tcp", "FromPort": 3001, "ToPort": 3001, "IpRanges": [{"CidrIp": "0.0.0.0/0"}]},
        {"IpProtocol": "tcp", "FromPort": 3002, "ToPort": 3002, "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}
    ]
)
print(f"✅ Created Security Group: {sg_id}")

# Step 4: Create Auto Scaling Group (ASG)
launch_template = autoscaling_client.create_launch_configuration(
    LaunchConfigurationName="backend-launch-template",
    ImageId="ami-08b5b3a93ed654d19",  # Replace with a valid AMI ID  (using amazon-linux)
    InstanceType="t2.micro",
    SecurityGroups=[sg_id],
    KeyName="my-key-pair",  # Replace with your actual key pair
)

autoscaling_client.create_auto_scaling_group(
    AutoScalingGroupName="backend-asg",
    LaunchConfigurationName="backend-launch-template",
    MinSize=1,
    MaxSize=3,
    DesiredCapacity=2,
    VPCZoneIdentifier=subnet_id,
    Tags=[{"Key": "Name", "Value": "Backend-Instance"}]
)

print("✅ Auto Scaling Group Created with EC2 instances running backend services.")
