#!/bin/bash

RESOURCE_GP=az-blob-rg
ACCT_NAME=sunny0storage0acct
CONTAINER_NAME=hw5-az-cli-0
LOCATION=westus2

function container_exists() {
  # Check whether the container already exists.
  # output is ignored - we're interested only in the return code.

   if (az storage blob list \
    --account-name $ACCT_NAME \
    --container-name $CONTAINER_NAME \
    --output none \
    --auth-mode login); then
    return 0 # 0 in Bash script means true.
  else
    return 1 # 1 in Bash script means false.
  fi
}

check_container () {

  if (container_exists); then
    # container exist, done
    return 0 
  fi

  # container doesn't exist, create it
  # create resoure group
  response=$(az group create --name "$RESOURCE_GP" --location "$LOCATION")
  # shellcheck disable=SC2181
  if [[ ${?} -ne 0 ]]; then
    echo "ERROR: Azure reports create resource group operation failed. $response"
    return 1
  fi

  # create a storage account
  response=$(az storage account create \
    --name $ACCT_NAME \
    --resource-group $RESOURCE_GP \
    --location $LOCATION \
    --sku Standard_ZRS \
    --encryption-services blob)
  # shellcheck disable=SC2181
  if [[ ${?} -ne 0 ]]; then
    echo "ERROR: Azure reports create storage acct operation failed. $response"
    return 1
  fi  
  acct_id=$(jq -r '.id' <<< "$response")

  # create container
  response=$(az ad signed-in-user show --query id -o tsv | az role assignment create \
    --role "Storage Blob Data Contributor" \
    --assignee @- \
    --scope "$acct_id")
  # shellcheck disable=SC2181
  if [[ ${?} -ne 0 ]]; then
    echo "ERROR: Azure reports create role operation failed. $response"
    return 1
  fi  

  response=$(az storage container create \
    --account-name $ACCT_NAME \
    --name $CONTAINER_NAME \
    --auth-mode login)
  # shellcheck disable=SC2181
  if [[ ${?} -ne 0 ]]; then
    echo "ERROR: Azure reports create container operation failed. $response"
    return 1
  fi  

  return 0
}

create_user_acct () {
  name="$1"
  password="$2"
  email="$3"
  user_acct_file="/tmp/$name"
  user_acct_obj="users/$name"

  #create temp user acct file
  echo "$name $password $email" > "$user_acct_file"

  response=$(az storage blob upload --account-name $ACCT_NAME \
    --container-name $CONTAINER_NAME \
    --name "$user_acct_obj" \
    --file "$user_acct_file" \
    --auth-mode login \
    --overwrite True)
  # shellcheck disable=SC2181
  if [[ $? -ne 0 ]]; then
    echo "ERROR:  Azure reports blob upload operation failed. $response"
    return 1
  fi

  return 0 
}

if [ $# -ne 3 ]; then
    echo "Usage: $0 <user-name> <password> <email>"
    exit 0
fi

if (check_container); then
  if (create_user_acct "$1" "$2" "$3"); then
    echo "user $1 created"
    exit 0
  fi
fi
echo "failed to create user $1"
