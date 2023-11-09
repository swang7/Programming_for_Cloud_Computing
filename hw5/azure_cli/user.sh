#!/bin/bash

USER_DIR="users/"

function get_user_info() {
    local acct_name
    local folder_name
    local user
    acct_name=$1
    folder_name=$2
    user=$3

    az storage blob download --account-name "$acct_name" \
        --container-name "$folder_name" \
        --name "$USER_DIR$user" \
        --file "/tmp/$user" \
        --output none \
        --auth-mode login > /dev/null 2>&1
    
    # shellcheck disable=SC2181
    if [[ ${?} -eq 0 ]]; then
        return 0 # 0 in Bash script means true.
    else
        return 1 # 1 in Bash script means false.
    fi
}

function auth_user() {
    local acct_name
    local folder_name
    local user
    acct_name=$1
    folder_name=$2
    user=$3
    user_pw=$4

    if ! (get_user_info "$acct_name" "$folder_name" "$user"); then
        return 1
    fi

    # get user info as an array
    read -r -a user_data < "/tmp/$user"
    
    if [[ $user == "${user_data[0]}" ]]  && [[ $user_pw == "${user_data[1]}" ]]; then
        return 0
    fi

    return 1
}