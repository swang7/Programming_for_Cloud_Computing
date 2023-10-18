#!/bin/bash

KEY_PAIR="aws-hw-keypair"

# create key pair
function create_key_pair() {
    aws ec2 create-key-pair --key-name "$KEY_PAIR"
    if [[ ${?} -eq 0 ]]; then
        echo "created key pair $KEY_PAIR"
        return 0 # 0 in Bash script means true.
    else
        return 1 # 1 in Bash script means false.
    fi
}

function key_pair_exist() {
    aws ec2 describe-key-pairs --key-names "$KEY_PAIR"
    if [[ ${?} -eq 0 ]]; then
        return 0 # 0 in Bash script means true.
    else
        return 1 # 1 in Bash script means false.
    fi
}

if !(key_pair_exist); then
    create_key_pair
fi
