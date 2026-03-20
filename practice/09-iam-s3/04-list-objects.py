#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError

bucket_name = "ds2002-khs3z"        # update this to the bucket you want to use, make sure it exists
prefix = ""    # update this to the prefix you want to use, make sure it is a valid prefix for the bucket

try:
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    contents = response.get("Contents", [])
    if not contents:
        print("No objects found.")
    else:
        print(f"Objects in s3://{bucket_name}/{prefix}")
        for obj in contents:
            print(f"- {obj['Key']} ({obj['Size']} bytes)")
except ClientError as e:
    print(f"Error listing objects: {e}")

