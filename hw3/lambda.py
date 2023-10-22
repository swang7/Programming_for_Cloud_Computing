import json
import boto3

def lambda_handler(event, context):

    print(event)
    event_name = event['Records'][0]['eventName']
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    obj_name = event['Records'][0]['s3']['object']['key']
    print(f"S3 event : {event_name}")
    print(f"S3 Bucket Name : {source_bucket}")
    print(f"S3 object : {obj_name}")

    ses = boto3.client('ses')
    subject = f"New object {obj_name} received on {source_bucket}"
    body = f"<br> Bucket Name : {source_bucket} <br> Action : {event_name} <br> Object Name : {obj_name}"

    
    response = ses.send_email(
        Source = "swancawan@gmail.com", 
        Destination = {
            'ToAddresses': ["sunnyyw@comcast.net"]
            },
        Message = {
            'Subject' : {
                'Data': subject
            },
            'Body': {
                'Html': {
                    'Data': body
                } 
            }
        }
    )
    print(f"send email: {response}")


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

