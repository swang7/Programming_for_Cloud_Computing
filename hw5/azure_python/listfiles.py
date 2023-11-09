
import logging
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import sys

import user

ACCT_NAME="sunny0storage0acct"
CONTAINER_NAME="hw5-az-python-0"

def get_files(blob_service_client, container_name, name):
    file_names = []

    try:
        container_client = blob_service_client.get_container_client(container= container_name) 

        # List the blobs in the container
        blob_list = container_client.list_blobs(name_starts_with=name)
        for blob in blob_list:
            file_names.append(blob.name)
    except Exception as ex:
        logging.error(ex)

    return file_names

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <user-name> <password>")
        sys.exit()

    try:
        account_url = "https://" + ACCT_NAME + ".blob.core.windows.net"
        default_credential = DefaultAzureCredential()

        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient(account_url, credential=default_credential)

        if not user.auth_user(blob_service_client, CONTAINER_NAME, sys.argv[1], sys.argv[2]):
            print(f"User {sys.argv[1]} not found or incorrect password")
            return

        file_names = get_files(blob_service_client, CONTAINER_NAME, sys.argv[1])
        for fname in file_names:
            print(fname.removeprefix(sys.argv[1] + "/"))

    except Exception as ex:
        logging.error(ex)
    
if __name__ == "__main__":
    main()
