#!/usr/bin/env python3
"""Launch one EC2 instance using an existing subnet and security group(s)."""

from pathlib import Path

import boto3
from botocore.exceptions import ClientError

# --- edit these values for your account ---
REGION = "us-east-1"
IMAGE_ID = "ami-0123456789abcdef0"
INSTANCE_TYPE = "t2.nano"
KEY_NAME = "my-key-pair"
SUBNET_ID = "subnet-0123456789abcdef0"
SECURITY_GROUP_IDS = [
    "sg-0123456789abcdef0",
]
INSTANCE_NAME = "ds2002-demo"  # set to "" to skip Name tag
USER_DATA_FILE = ""  # e.g. "bootstrap.sh"; leave "" for none

ec2 = boto3.client("ec2", region_name=REGION)

run_kw = {
    "ImageId": IMAGE_ID,
    "MinCount": 1,
    "MaxCount": 1,
    "InstanceType": INSTANCE_TYPE,
    "KeyName": KEY_NAME,
    "SubnetId": SUBNET_ID,
    "SecurityGroupIds": SECURITY_GROUP_IDS,
}
if INSTANCE_NAME:
    run_kw["TagSpecifications"] = [
        {
            "ResourceType": "instance",
            "Tags": [{"Key": "Name", "Value": INSTANCE_NAME}],
        }
    ]
if USER_DATA_FILE:
    run_kw["UserData"] = Path(USER_DATA_FILE).read_text(encoding="utf-8")

try:
    response = ec2.run_instances(**run_kw)
except ClientError as exc:
    raise SystemExit(f"run_instances failed: {exc}") from exc

instance = response["Instances"][0]
print(instance["InstanceId"], instance["State"]["Name"])
