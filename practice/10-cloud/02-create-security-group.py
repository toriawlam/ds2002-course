#!/usr/bin/env python3
"""Create a VPC security group and add an inbound SSH (port 22) rule."""

import boto3
from botocore.exceptions import ClientError

# --- edit these values for your account / VPC ---
REGION = "us-east-1"
VPC_ID = "vpc-0123456789abcdef0"
GROUP_NAME = "ds2002-sg-mst3k"
DESCRIPTION = "Created by 02-create-security-group.py"
# Who may reach SSH on the instance: CIDR block (e.g. your home/office /32, or 0.0.0.0/0 for “anywhere”).
SSH_CIDR = "0.0.0.0/0"  # narrow to your IP in production

# EC2 API client; region must match the VPC and any instances you attach this group to.
ec2 = boto3.client("ec2", region_name=REGION)

# Step 1: Register a new security group in the VPC. A security group is a stateful
# firewall attached to ENIs/instances: it starts with no inbound rules (implicit deny).
try:
    created = ec2.create_security_group(
        GroupName=GROUP_NAME,
        Description=DESCRIPTION,
        VpcId=VPC_ID,
    )
except ClientError as exc:
    raise SystemExit(f"create_security_group failed: {exc}") from exc

sg_id = created["GroupId"]

# Step 2: Add an inbound (ingress) rule so TCP port 22 (SSH) is allowed from SSH_CIDR.
# Outbound traffic is allowed by default unless you remove the default egress rule later.
try:
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 22,
                "ToPort": 22,
                "IpRanges": [{"CidrIp": SSH_CIDR, "Description": "SSH"}],
            }
        ],
    )
except ClientError as exc:
    raise SystemExit(f"authorize_security_group_ingress failed: {exc}") from exc

# Print the new sg-… id so you can copy it into SECURITY_GROUP_IDS in 03-launch-instance.py.
print(sg_id)
