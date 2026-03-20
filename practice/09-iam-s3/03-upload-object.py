#!/usr/bin/env python3

import os
import boto3
from botocore.exceptions import ClientError

bucket_name = "mybucket-" + os.environ.get("USER")           # update this to the bucket you want to use, make sure it exists
local_file = "cloud.jpg"      # update this to the file you want to upload, make sure it exists in the current directory
key = "folder/in/bucket/cloud.jpg"  # update this to the key you want to use, make sure it is a valid key for the bucket

try:
    s3 = boto3.client("s3")
    with open(local_file, "rb") as f:
        s3.put_object(Bucket=bucket_name, Key=key, Body=f)
    print(f"Uploaded {local_file} to s3://{bucket_name}/{key}")
except FileNotFoundError:
    print(f"Local file not found: {local_file}")
except ClientError as e:
    print(f"Error uploading object: {e}")

