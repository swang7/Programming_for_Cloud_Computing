import logging
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import sys

import user

ACCT_NAME="sunny0storage0acct"
CONTAINER_NAME="hw5-az-python-0"

def upload_file(blob_service_client, container_name, fname, blob_name):

    try:
        # Create a blob client using the blob name
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # Upload the created file
        with open(file=fname, mode="rb") as data:
            blob_client.upload_blob(data)
    except Exception as ex:
        logging.error(ex)
        return False

    return True

def main():
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <user-name> <password> <file-key> <path-to-file-to-upload>")
        sys.exit()

    try:
        account_url = "https://" + ACCT_NAME + ".blob.core.windows.net"
        default_credential = DefaultAzureCredential()

        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient(account_url, credential=default_credential)
        if user.auth_user(blob_service_client, CONTAINER_NAME, sys.argv[1], sys.argv[2]):
            # store user file under user-name folder
            file_key = sys.argv[1] + "/" + sys.argv[3]
            if upload_file(blob_service_client, CONTAINER_NAME, sys.argv[4], file_key):
                print("file uploaded")
                return
            
    except Exception as ex:
        logging.error(ex)

    print("file upload failed")

if __name__ == "__main__":
   main()