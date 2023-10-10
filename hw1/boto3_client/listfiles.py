
import logging
import boto3
from botocore.exceptions import ClientError
import os
import sys

import user

BUCKET_NAME="aws-hw1-boto3-client-0"

def get_files(s3_client, bucket_name, prefix=""):
    file_names = []

    default_kwargs = {
        "Bucket": bucket_name,
        "Prefix": prefix
    }
    next_token = ""

    while next_token is not None:
        updated_kwargs = default_kwargs.copy()
        if next_token != "":
            updated_kwargs["ContinuationToken"] = next_token

        response = s3_client.list_objects_v2(**updated_kwargs)
        contents = response.get("Contents")

        if contents is not None:
            for result in contents:
                key = result.get("Key")
                if key[-1] != "/":
                    file_names.append(key)

        next_token = response.get("NextContinuationToken")

    return file_names

def main():
    if (args_count := len(sys.argv)) != 3:
        print(f"Usage: {sys.argv[0]} <user-name> <password>")
        sys.exit()

    client = boto3.client("s3")
        
    if not user.auth_user(client, BUCKET_NAME, sys.argv[1], sys.argv[2]):
        print(f"User {sys.argv[1]} not found or incorrect password")
        return

    file_names = get_files(client, BUCKET_NAME, sys.argv[1])
    for fname in file_names:
        print(fname.removeprefix(sys.argv[1] + "/"))

if __name__ == "__main__":
    main()
