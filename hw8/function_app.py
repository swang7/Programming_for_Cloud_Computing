import azure.functions as func
import logging

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="from-container/{name}",
                connection="AzureWebJobsStorage")
@app.blob_output(arg_name="blobout",
                path="to-container/{name}",
                connection="AzureWebJobsStorage")
def BlobCopy(myblob: func.InputStream, blobout: func.Out[func.InputStream]):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
    blobout.set(myblob)
