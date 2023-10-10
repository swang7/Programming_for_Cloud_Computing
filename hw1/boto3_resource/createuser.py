import logging
import boto3
from botocore.exceptions import ClientError
import sys

import user

BUCKET_NAME="aws-hw1-boto3-resource-0"

def check_bucket(s3):

    bucket = s3.Bucket(BUCKET_NAME)
    if bucket.creation_date is None:
        bucket.create(
            CreateBucketConfiguration={
                'LocationConstraint': 'us-west-2',    
            },
        )
    return True

def main():
    if (args_count := len(sys.argv)) != 4:
        print(f"Usage: {sys.argv[0]} <user-name> <password> <email>")
        sys.exit()

    s3 = boto3.resource("s3")
    if check_bucket(s3):
        if user.create_user(s3, BUCKET_NAME, sys.argv[1], sys.argv[2], sys.argv[3]):
            print(f"user created")
            return
    
    print("create user failed")

if __name__ == "__main__":
    main()