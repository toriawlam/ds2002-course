#!/usr/bin/env python3

import boto3

s3 = boto3.client("s3")
response = s3.list_buckets()
buckets = response.get("Buckets", [])

if not buckets:
    print("No buckets found.")
else:
    print("Buckets:")
    for b in buckets:
        print(f"- {b['Name']}")

