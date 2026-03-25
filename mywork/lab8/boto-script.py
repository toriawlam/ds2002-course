#!/usr/bin/env python

import boto3

s3 = boto3.client('s3', region_name='us-east-1')

# response = s3.list_buckets()

# to print all bucket names in a full json payload, all results in an array
# for r in response['Buckets']:
#     print(r['Name'])

# to upload a file to your bucket
bucket = 'ds2002-kze4za'
local_file = 'uva.jpg'

with open(local_file, 'rb') as f:
    s3.put_object(
        Body = f,
        Bucket = bucket,
        Key = local_file,
        ACL = 'public-read',
    )

# tried response, but wouldn't let me view the image