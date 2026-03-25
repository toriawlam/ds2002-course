#!/usr/bin/env python3
"""List EC2 instances visible to your credentials (describe_instances)."""

import boto3
from botocore.exceptions import ClientError

# --- edit if your resources are in another region ---
REGION = "us-east-1"

def _name_from_tags(tags) -> str:
    if not tags:
        return ""
    for tag in tags:
        if tag.get("Key") == "Name":
            return tag.get("Value") or ""
    return ""


ec2 = boto3.client("ec2", region_name=REGION)
try:
    response = ec2.describe_instances()
except ClientError as exc:
    raise SystemExit(f"describe_instances failed: {exc}") from exc

for reservation in response["Reservations"]:
    for inst in reservation["Instances"]:
        iid = inst["InstanceId"]
        state = inst["State"]["Name"]
        itype = inst.get("InstanceType", "")
        pub = inst.get("PublicIpAddress") or "-"
        name = _name_from_tags(inst.get("Tags"))
        print(iid, state, itype, pub, name)


