#!/bin/bash

source ./user.sh

ACCT_NAME=sunny0storage0acct
CONTAINER_NAME=hw5-az-cli-0

function get_files() {
    local acct_name
    local container_name
    local user
    acct_name=$1
    container_name=$2
    user=$3

    response=$(az storage blob list \
    --account-name "$acct_name" \
    --container-name "$container_name" \
    --prefix "$user" \
    --output table \
    --auth-mode login)
 
    str_len=$(( ${#user} + 1 ))
    str_pad=$(printf "%*s" $str_len)

    # remove user folder prefix when list files
    echo "${response//${user}\//$str_pad}"
}

if [ $# -ne 2 ]; then
    echo "Usage: $0 <user-name> <password>"
    exit 0
fi

if ! (auth_user $ACCT_NAME $CONTAINER_NAME "$1" "$2"); then 
    echo "user not found or incorrect password"
fi

get_files $ACCT_NAME $CONTAINER_NAME "$1"