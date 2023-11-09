import logging
import sys
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

import user

ACCT_NAME="sunny0storage0acct"
CONTAINER_NAME="hw5-az-python-0"

def container_exists(blob_service_client, container_name):
    try:
        container_client = blob_service_client.get_container_client(container_name)
        if container_client.exists():
            return True
    except Exception as ex:
        logging.error(ex)
        return False
    
def check_container(blob_service_client, container_name):

    if container_exists(blob_service_client, container_name):
        return True

    # create container for storage system
    try:
        # Create the container
        blob_service_client.create_container(container_name)
        return True
    except Exception as ex:
        logging.error(ex)
        return False

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <user-name> <password> <email>")
        sys.exit()

    try:
        account_url = "https://" + ACCT_NAME + ".blob.core.windows.net"
        default_credential = DefaultAzureCredential()

        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient(account_url, credential=default_credential)
        if check_container(blob_service_client, CONTAINER_NAME):
            if user.create_user(blob_service_client, CONTAINER_NAME, sys.argv[1], sys.argv[2], sys.argv[3]):
                print(f"user created")
                return
        
    except Exception as ex:
        logging.error(ex)
    
    print("create user failed")

if __name__ == "__main__":
    main()