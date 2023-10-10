import logging
import boto3
from botocore.exceptions import ClientError
import os
import sys

USERS_DIR="users/"

def get_user_info(s3, bucket, name):

    fname = "/tmp/" + name

    try:
        s3.Object(bucket, USERS_DIR + name).download_file(fname)
    except ClientError as e:
        logging.error(e)
        return []

    # opening the file in read mode 
    user_file = open(fname, "r") 
  
    # reading the file 
    data = user_file.read()
    user_file.close()

    return data.split()

def auth_user(s3, bucket, name, passwd):

    data = get_user_info(s3, bucket, name)
    # print(f"user info:", data)

    # data = [user_name, passwd, email]
    if len(data):
        if name == data[0] and passwd == data[1]:
            return True
        
    return False

def create_user(s3, bucket, name, pswd, email):

    fname = "/tmp/" + name
    user_file = open(fname, "w")
    data = name + " " + pswd + " " + email
    user_file.write(data)
    user_file.close()

    object_name = USERS_DIR + name

    try:
        s3.Bucket(bucket).upload_file(fname, object_name)
    except ClientError as e:
        logging.error(e)
        #clean up file
        os.remove(fname)
        return False

    # clean up file
    os.remove(fname)
    return True
