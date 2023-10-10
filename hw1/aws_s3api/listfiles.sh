#!/bin/bash

source ./user.sh

BUCKET_NAME=aws-hw1-bucket-aws-c3api-0

function get_files() {
    local bucket_name
    local user
    bucket_name=$1
    user=$2/

    response=$(aws s3api list-objects --bucket $bucket_name --prefix "$user" --query 'Contents[].{Key: Key}' --output text)

    if [[ $response == $user* ]]; then
        # remove user folder prefix when list files
        echo "${response//${user}/}"
    fi
}

if [ $# -ne 2 ]; then
    echo "Usage: $0 <user-name> <password>"
    exit 0
fi

if !(auth_user $BUCKET_NAME $1 $2); then 
    echo "user not found or incorrect password"
fi

get_files $BUCKET_NAME $1
