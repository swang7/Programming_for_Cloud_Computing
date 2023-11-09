
import logging
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import sys

import user

ACCT_NAME="sunny0storage0acct"
CONTAINER_NAME="hw5-az-python-0"

def download_file(blob_service_client, container_name, blob_name, fname):
    try:
        container_client = blob_service_client.get_container_client(container_name)

        with open(file=fname, mode="wb") as download_file:
            download_file.write(container_client.download_blob(blob_name).readall())
    except Exception as ex:
        logging.error(ex)
        return False
    
    return True

def main():
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <user-name> <password> <file-key> <path-to-save-file-to>")
        sys.exit()

    try:
        account_url = "https://" + ACCT_NAME + ".blob.core.windows.net"
        default_credential = DefaultAzureCredential()

        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient(account_url, credential=default_credential)

        if not user.auth_user(blob_service_client, CONTAINER_NAME, sys.argv[1], sys.argv[2]):
            print(f"User {sys.argv[1]} not found or incorrect password")
            return
        
        # user files stored under user-name folder
        file_key = sys.argv[1] + "/" + sys.argv[3]

        if download_file(blob_service_client, CONTAINER_NAME, file_key, sys.argv[4]):
            print(f"File {sys.argv[3]} downloaded to {sys.argv[4]}")
        else:
            print(f"Error downloading file {sys.argv[3]} to {sys.argv[4]}")
    except Exception as ex:
        logging.error(ex)

if __name__ == "__main__":
    main()