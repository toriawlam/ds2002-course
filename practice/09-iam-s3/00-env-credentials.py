#!/usr/bin/env python3

import os
import boto3

# Assume the following environment variables are set:
# export MY_ACCESS_KEY="YOUR_KEY"
# export MY_SECRET_ACCESS_KEY="YOUR_SECRET"

ACCESS_KEY = os.getenv("MY_ACCESS_KEY")
SECRET_ACCESS_KEY = os.getenv("MY_SECRET_ACCESS_KEY")
s3 = boto3.client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
)