#!/bin/bash

source ./user.sh

BUCKET_NAME=aws-hw1-bucket-aws-cli-0

function get_file() {
    local bucket_name
    local user
    bucket_name=$1
    user="$2"
    user_file="$3"
    user_obj="$4"

    response=$(aws s3 cp "s3://$bucket_name/$user_obj" "$user_file")

    if [[ $? -ne 0 ]]; then
        echo "ERROR:  AWS reports s3 cp operation failed.\n$response"
        return 1
    fi
    return 0
}

if [ $# -ne 4 ]; then
    echo "Usage: $0 <user-name> <password> <file-key> <path-to-save-file-to>"
    exit 0
fi

if !(auth_user $BUCKET_NAME $1 $2); then 
    echo "user not found or incorrect password"
fi

file_key=$1/$3
if (get_file $BUCKET_NAME "$1" "$4" "$file_key"); then
    echo "file downloaded"
else
    echo "file download failed"
fi