import boto3
import urllib.parse
import os

s3 = boto3.client("s3")
DESTINATION_BUCKET = os.environ["DESTINATION_BUCKET"]


def lambda_handler(event, context):
    # Get the source bucket and object key from the event
    source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )

    copy_source = {"Bucket": source_bucket, "Key": object_key}

    # Check to prevent infinite loops if source and destination are the same bucket without a prefix filter
    if source_bucket == DESTINATION_BUCKET:
        print("Source and destination buckets are the same. Aborting copy operation.")
        return

    print(f"Copying {object_key} from {source_bucket} to {DESTINATION_BUCKET}")

    try:
        s3.copy_object(
            CopySource=copy_source, Bucket=DESTINATION_BUCKET, Key=object_key
        )
        print("S3 object copy successful.")
        return {"status": "success"}
    except Exception as e:
        print(f"Error copying object: {e}")
        raise e
