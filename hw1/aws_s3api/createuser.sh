#!/bin/bash

BUCKET_NAME=aws-hw1-bucket-aws-c3api-0

function bucket_exists() {
  local bucket_name
  bucket_name=$1

  # Check whether the bucket already exists.
  # We suppress all output - we're interested only in the return code.

  aws s3api head-bucket \
    --bucket "$bucket_name" \
    >/dev/null 2>&1

  if [[ ${?} -eq 0 ]]; then
    return 0 # 0 in Bash script means true.
  else
    return 1 # 1 in Bash script means false.
  fi
}

check_bucket () {

  if (bucket_exists "$BUCKET_NAME"); then
    # bucket exist, done
    return 0 
  fi

  # bucket doesn't exist, create it
  response=$(aws s3api create-bucket --bucket "$BUCKET_NAME" --region "us-west-2" \
    --create-bucket-configuration LocationConstraint=us-west-2)

  if [[ ${?} -ne 0 ]]; then
    echo "ERROR: AWS reports create-bucket operation failed.\n$response"
    return 1
  fi

  return 0
}

create_user_acct () {
  name=$1
  password=$2
  email=$3
  user_acct_file="/tmp/$name"
  user_acct_obj="users/$name"

  #create temp user acct file
  echo "$name $password $email" > $user_acct_file

  response=$(aws s3api put-object --bucket "$BUCKET_NAME" --key "$user_acct_obj" \
    --body "$user_acct_file")

  # shellcheck disable=SC2181
  if [[ $? -ne 0 ]]; then
    echo "ERROR:  AWS reports s3api put-object operation failed.\n$response"
    return 1
  fi

  # remove /tmp/$name
  rm "$user_acct_file"
  return 0 
}

if [ $# -ne 3 ]; then
    echo "Usage: $0 <user-name> <password> <email>"
    exit 0
fi

if (check_bucket); then
  if (create_user_acct $1 $2 $3); then
    echo "user $1 created"
    exit 0
  fi
fi
echo "failed to create user $1"
