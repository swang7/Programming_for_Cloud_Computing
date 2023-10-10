
import logging
import boto3
from botocore.exceptions import ClientError
import os
import sys

import user

BUCKET_NAME="aws-hw1-boto3-resource-0"

def get_files(s3, bucket_name, prefix):
    file_names = []

    bucket = s3.Bucket(bucket_name)
    object_iterator = bucket.objects.filter(Prefix=prefix)

    for bucket_object in object_iterator:
        file_names.append(bucket_object.key)

    return file_names

def main():
    if (args_count := len(sys.argv)) != 3:
        print(f"Usage: {sys.argv[0]} <user-name> <password>")
        sys.exit()

    s3 = boto3.resource("s3")
    if not user.auth_user(s3, BUCKET_NAME, sys.argv[1], sys.argv[2]):
        print(f"User {sys.argv[1]} not found or incorrect password")
        return

    file_names = get_files(s3, BUCKET_NAME, sys.argv[1])
    for fname in file_names:
        print(fname.removeprefix(sys.argv[1] + "/"))

if __name__ == "__main__":
    main()