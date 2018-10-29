import os
import io
import boto3
import json
import csv
import base64

# environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime = boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    print("*** Raw Event: ", event)

    data = json.loads(json.dumps(event))
    encoded_body = data['body']
    decoded_body = base64.b64decode(encoded_body)

    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME, 
                                       Body=decoded_body)
    print("***Response: ", response)
    
    csv_result = response['Body'].read().decode('utf-8')

    print("*** CSV: \n", csv_result)
    
    r_meta = response['ResponseMetadata']
    print("*** Response Status Code: ", r_meta['HTTPStatusCode'])

    
    handler_response = {"isBase64Encoded": False,
                        "statusCode": r_meta['HTTPStatusCode'],
                        "headers": {"content-type": 'application/json'},
                        "body": json.dumps({"results": csv_result})}
                        
    return handler_response
