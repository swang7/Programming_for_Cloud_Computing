#!/bin/bash

source ./user.sh

BUCKET_NAME=aws-hw1-bucket-aws-c3api-0

function upload_file() {
    local bucket_name
    local user
    bucket_name=$1
    user=$2
    user_file=$3
    user_obj=$4

    response=$(aws s3api put-object --bucket $bucket_name --key "$user_obj" \
        --body "$user_file")

    if [[ $? -ne 0 ]]; then
        echo "ERROR:  AWS reports s3api put-object operation failed.\n$response"
        return 1
    fi
    return 0
}

if [ $# -ne 4 ]; then
    echo "Usage: $0 <user-name> <password> <file-key> <path-to-file-to-upload>"
    exit 0
fi

if !(auth_user $BUCKET_NAME $1 $2); then 
    echo "user not found or incorrect password"
fi

file_key=$1/$3
if (upload_file $BUCKET_NAME $1 "$4" "$file_key"); then
    echo "file uploaded"
else
    echo "file upload failed"
fi