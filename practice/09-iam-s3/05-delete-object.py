#!/usr/bin/env python3

import os
import boto3
from botocore.exceptions import ClientError

bucket_name = "mybucket-" + os.environ.get("USER") # update this to the bucket you want to use, make sure it exists
key = "folder/in/bucket/file.txt" # update this to the key you want to use, make sure it is a valid key for the bucket

try:
    s3 = boto3.client("s3")
    s3.delete_object(Bucket=bucket_name, Key=key)
    print(f"Deleted s3://{bucket_name}/{key}")
except ClientError as e:
    print(f"Error deleting object: {e}")
