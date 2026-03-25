#!/usr/bin/env python

# add imports here
from pathlib import Path
import argparse
import logging
import os
import boto3

# instantiate logger
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[console_handler])

def parse_args():
    # parse command line arguments
    # return input folder and bucket/prefix destination
    parser = argparse.ArgumentParser(description="parses through input arguments")
    parser.add_argument("input_folder",help="input folder")
    parser.add_argument("bucket_destination",help="bucket destination")

    args = parser.parse_args()
    return args.input_folder, args.bucket_destination

def upload(input_folder, destination):
    # accepts 2 arguments: input_folder, destination
    try:
        s3 = boto3.client('s3', region_name='us-east-1')

        bucket, prefix = destination.split("/", 1)
        folder = Path(input_folder)

        for file in folder.glob("results*.csv"):
            key = f"{prefix}/{file.name}"
            logger.info(f"Uploading {file} to s3://{bucket}/{key}")
            s3.upload_file(str(file), bucket, key)
        
        return True

    except Exception as e:
        logger.error("Upload failed: ", e)
        return False

def main():
    input_folder, destination = parse_args()
    status = upload(input_folder, destination)
    if status:
        logger.info("All files uploaded")
    else:
        logger.error("File upload failed")

if __name__ == "__main__":
    main()
