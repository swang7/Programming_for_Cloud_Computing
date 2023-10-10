import logging
import boto3
from botocore.exceptions import ClientError
import sys

import user

BUCKET_NAME="aws-hw1-boto3-client-0"

def bucket_exists(s3):
    try:
        s3.head_bucket(Bucket=BUCKET_NAME)
        return True
    except ClientError as e:
        return False

def check_bucket(s3):

    if bucket_exists(s3):
        return True

    # create bucket for storage system
    try:
        s3.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={
                'LocationConstraint': 'us-west-2',    
            },
        )
        return True
    except ClientError as e:
        logging.error(e)
        return False


def main():
    if (args_count := len(sys.argv)) != 4:
        print(f"Usage: {sys.argv[0]} <user-name> <password> <email>")
        sys.exit()

    client = boto3.client("s3")
    if check_bucket(client):
        if user.create_user(client, BUCKET_NAME, sys.argv[1], sys.argv[2], sys.argv[3]):
            print(f"user created")
            return
    
    print("create user failed")

if __name__ == "__main__":
    main()