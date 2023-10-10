#!/bin/bash

USER_DIR="users/"

function get_user_info() {
    local bucket
    local user
    bucket_name=$1
    user=$2

    response=$(aws s3api get-object --bucket "$bucket_name" --key "$USER_DIR$user" "/tmp/$user" >/dev/null 2>&1)

    if [[ ${?} -eq 0 ]]; then
        return 0 # 0 in Bash script means true.
    else
        #echo "ERROR:  AWS reports s3api get-object operation failed.\n$response"
        return 1 # 1 in Bash script means false.
    fi
}

function auth_user() {
    local bucket
    local user
    bucket_name=$1
    user=$2
    user_pw=$3

    if !(get_user_info $bucket_name $user); then
        return 1
    fi

    # get user info as an array
    user_data=( $(cat "/tmp/$user") )
    if [[ $user = ${user_data[0]} && $user_pw = ${user_data[1]} ]]; then
        return 0
    fi

    return 1
}

# if (auth_user $BUCKET_NAME $1 $2); then 
#     echo "user authenticated"; 
# else
#     echo "user not found or invalid password"
# fi