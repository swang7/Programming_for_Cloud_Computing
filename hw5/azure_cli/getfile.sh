#!/bin/bash

source ./user.sh

ACCT_NAME=sunny0storage0acct
CONTAINER_NAME=hw5-az-cli-0

function get_file() {
    local acct_name
    local container_name
    local user_file
    local user_blob
    acct_name="$1"
    container_name="$2"
    user_file="$3"
    user_blob="$4"

    response=$(az storage blob download --account-name "$acct_name" \
        --container-name "$container_name" \
        --name "$user_blob" \
        --file "$user_file" \
        --output none \
        --auth-mode login)
    # shellcheck disable=SC2181
    if [[ $? -ne 0 ]]; then
        echo "ERROR:  Azure reports blob download operation failed. $response"
        return 1
    fi
    return 0
}

if [ $# -ne 4 ]; then
    echo "Usage: $0 <user-name> <password> <file-key> <path-to-save-file-to>"
    exit 0
fi

if ! (auth_user $ACCT_NAME $CONTAINER_NAME "$1" "$2"); then 
    echo "user not found or incorrect password"
fi

file_key=$1/$3
if (get_file $ACCT_NAME $CONTAINER_NAME "$4" "$file_key"); then
    echo "file downloaded"
else
    echo "file download failed"
fi