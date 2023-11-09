import logging
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

USERS_DIR="users/"

def get_user_info(blob_service_client, container_name, name):

    blob_name = USERS_DIR + name
    try:
        container_client = blob_service_client.get_container_client(container_name)
        data = container_client.download_blob(blob_name).readall().decode('utf-8')
    except Exception as ex:
        #logging.error(ex)
        return []

    return data.split()

def auth_user(blob_service_client, container_name, name, passwd):

    data = get_user_info(blob_service_client, container_name, name)
    #print(f"user info:", data)

    if len(data):
        if name == data[0] and passwd == data[1]:
            return True
        
    return False

def create_user(blob_service_client, container_name, name, pswd, email):

    fname = "/tmp/" + name
    user_file = open(fname, "w")
    data = name + " " + pswd + " " + email
    user_file.write(data)
    user_file.close()

    blob_name = USERS_DIR + name

    try:
        # Create a blob client using the blob name
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        # Upload the created file
        with open(file=fname, mode="rb") as data:
            blob_client.upload_blob(data=data, overwrite=True)

    except Exception as ex:
        logging.error(ex)
        os.remove(fname)
        return False

    # clean up file
    os.remove(fname)
    return True
