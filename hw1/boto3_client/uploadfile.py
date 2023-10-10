import logging
import boto3
from botocore.exceptions import ClientError
import os
import sys

import user

BUCKET_NAME="aws-hw1-boto3-client-0"

def upload_file(s3, bucket, file_name, object_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name.
    :return: True if file was uploaded, else False
    """

    # Upload the file
    try:
        response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def main():
    if (args_count := len(sys.argv)) != 5:
        print(f"Usage: {sys.argv[0]} <user-name> <password> <file-key> <path-to-file-to-upload>")
        sys.exit()

    client = boto3.client("s3")
    if user.auth_user(client, BUCKET_NAME, sys.argv[1], sys.argv[2]):
        # store user file under user-name folder
        file_key = sys.argv[1] + "/" + sys.argv[3]
        if upload_file(client, BUCKET_NAME, sys.argv[4], file_key):
            print("file uploaded")
            return
    
    print("file upload failed")

if __name__ == "__main__":
   main()