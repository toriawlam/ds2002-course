#!/usr/bin/env python3
"""Terminate one or more EC2 instances by instance id."""

import boto3
from botocore.exceptions import ClientError

# --- edit these values; confirm ids before running (termination is permanent) ---
REGION = "us-east-1"
INSTANCE_IDS = [
    "i-0123456789abcdef0",
]

ec2 = boto3.client("ec2", region_name=REGION)

try:
    response = ec2.terminate_instances(InstanceIds=INSTANCE_IDS)
except ClientError as exc:
    raise SystemExit(f"terminate_instances failed: {exc}") from exc

for inst in response["TerminatingInstances"]:
    print(inst["InstanceId"], inst["CurrentState"]["Name"])
