#!/usr/bin/env python3

import os
import boto3
from botocore.exceptions import ClientError

bucket_name = "mybucket-" + os.environ.get("USER")
print (bucket_name)

try:
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)
    print(f"Created bucket: {bucket_name}")
except ClientError as e:
    print(f"Error creating bucket {bucket_name}: {e}")

