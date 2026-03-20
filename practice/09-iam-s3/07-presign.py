#!/usr/bin/env python3

import os
import boto3
from botocore.exceptions import ClientError

bucket_name = "mybucket-" + os.environ.get("USER")  # update this to the bucket you want to use, make sure it exists
key = "folder/in/bucket/cloud.jpg" # update this to the key you want to use, make sure it is a valid key for the bucket
expiration = 600 # update this to the number of seconds you want the presigned URL to be valid for

s3 = boto3.client("s3")
try:
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": key},
        ExpiresIn=expiration,
    )
    print(url)
except ClientError as e:
    print(f"Error generating presigned URL: {e}")
