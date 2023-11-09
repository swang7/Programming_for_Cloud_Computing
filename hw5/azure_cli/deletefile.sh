#!/bin/bash

source ./user.sh

ACCT_NAME=sunny0storage0acct
CONTAINER_NAME=hw5-az-cli-0

function delete_file() {
    local acct_name
    local container_name
    local user_blob
    acct_name=$1
    container_name=$2
    user_blob=$3

    response=$(az storage blob delete --account-name "$acct_name" \
        --container-name "$container_name" \
        --name "$user_blob" \
        --auth-mode login)
    # shellcheck disable=SC2181
    if [[ $? -ne 0 ]]; then
        echo "ERROR:  Azure reports blob delete operation failed. $response"
        return 1
    fi
    return 0
}

if [ $# -ne 3 ]; then
    echo "Usage: $0 <user-name> <password> <file-key>"
    exit 0
fi

if ! (auth_user $ACCT_NAME $CONTAINER_NAME "$1" "$2"); then 
    echo "user not found or incorrect password"
fi

file_key=$1/$3
if (delete_file $ACCT_NAME $CONTAINER_NAME "$file_key"); then
    echo "file \"$3\" deleted"
else
    echo "Error deleting file \"$3\""
fi