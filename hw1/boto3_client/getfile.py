
import logging
import boto3
from botocore.exceptions import ClientError
import os
import sys

import user

BUCKET_NAME="aws-hw1-boto3-client-0"

def download_file(s3, bucket, obj_name, fname):
    try:
        s3.download_file(bucket, obj_name, fname)
    except ClientError as e:
        logging.error(e)
        return False
    
    return True

def main():
    if (args_count := len(sys.argv)) != 5:
        print(f"Usage: {sys.argv[0]} <user-name> <password> <file-key> <path-to-save-file-to>")
        sys.exit()

    client = boto3.client("s3")
        
    if not user.auth_user(client, BUCKET_NAME, sys.argv[1], sys.argv[2]):
        print(f"User {sys.argv[1]} not found or incorrect password")
        return
    
    # user files stored under user-name folder
    file_key = sys.argv[1] + "/" + sys.argv[3]

    if download_file(client, BUCKET_NAME, file_key, sys.argv[4]):
        print(f"File {sys.argv[3]} downloaded to {sys.argv[4]}")
    else:
        print(f"Error downloading file {sys.argv[3]} to {sys.argv[4]}")

if __name__ == "__main__":
    main()