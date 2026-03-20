#!/usr/bin/env python3

import os
import boto3
from botocore.exceptions import ClientError

bucket_name = "mybucket-" + os.environ.get("USER") # update this to the bucket you want to use, make sure it exists
s3 = boto3.client("s3")

try:
    # note: bucket must be empty before it can be deleted
    #set short retention policy on the bucket
    s3.put_bucket_lifecycle_configuration(
        Bucket=bucket_name,
        LifecycleConfiguration={
            "Rules": [
                {
                    "ID": "short-retention",
                    "Prefix": "",
                    "Status": "Enabled",
                    "Expiration": {
                        "Days": 1
                    }
                }
            ]
        }
    )
    s3.delete_bucket(Bucket=bucket_name)
    print(f"Deleted bucket: {bucket_name}")
except ClientError as e:
    print(f"Error deleting bucket {bucket_name}: {e}")
