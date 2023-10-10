
import logging
import boto3
from botocore.exceptions import ClientError
import os
import sys

import user

BUCKET_NAME="aws-hw1-boto3-resource-0"

def delete_file(s3, bucket, obj_name):

    try:
        resp=s3.Bucket(bucket).delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': obj_name
                    },
                ],
            },
        )
    except ClientError as e:
        logging.error(e)
        return False
    
    return True

def main():
    if (args_count := len(sys.argv)) != 4:
        print(f"Usage: {sys.argv[0]} <user-name> <password> <file-key>")
        sys.exit()

    s3 = boto3.resource("s3")
        
    if not user.auth_user(s3, BUCKET_NAME, sys.argv[1], sys.argv[2]):
        print(f"User {sys.argv[1]} not found or incorrect password")
        return
    
    # user files stored under user-name folder
    file_key = sys.argv[1] + "/" + sys.argv[3]

    if delete_file(s3, BUCKET_NAME, file_key):
        print(f"File {sys.argv[3]} deleted")
    else:
        print(f"Error deleting file {sys.argv[3]}")

if __name__ == "__main__":
    main()
