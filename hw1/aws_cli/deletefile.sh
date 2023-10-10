#!/bin/bash

source ./user.sh

BUCKET_NAME=aws-hw1-bucket-aws-cli-0

function delete_file() {
    local bucket_name
    local user
    bucket_name=$1
    user=$2
    user_obj=$3

    response=$(aws s3 rm "s3://$bucket_name/$user_obj")

    if [[ $? -ne 0 ]]; then
        echo "ERROR:  AWS reports s3 rm operation failed.\n$response"
        return 1
    fi
    return 0
}

if [ $# -ne 3 ]; then
    echo "Usage: $0 <user-name> <password> <file-key>"
    exit 0
fi

if !(auth_user $BUCKET_NAME $1 $2); then 
    echo "user not found or incorrect password"
fi

file_key=$1/$3
if (delete_file $BUCKET_NAME $1 "$file_key"); then
    echo "file \"$3\" deleted"
else
    echo "Error deleting file \"$3\""
fi