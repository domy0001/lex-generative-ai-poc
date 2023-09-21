import io
import os
import gzip
import json
import boto3
import base64
import logging

logging.basicConfig(level=logging.DEBUG)
connect_client = boto3.client('connect')
s3_client = boto3.client('s3')

instance_id = os.environ['CONNECT_INSTANCE_ID']
print(f'Instance Id: {instance_id}')

def handler(event, context):
    logging.info(f'Event body: {str(event)}')
    try:
        #S3 event
        event_record = event['Records'][0]

        bucket_name = event_record['s3']['bucket']['name']
        object_key = event_record['s3']['object']['key']
        s3_response = get_object(bucket=bucket_name, key=object_key)
        encoded_inputs = s3_response['Body'].read().decode('utf-8')

        encoded_inputs = encoded_inputs.split(':')
        output = []
        flow_names = []
        for enc_input in encoded_inputs:
            enc_input = enc_input.split('-')
            flow_name = enc_input[0]
            flow_names.append(flow_name)
            flow_content = enc_input[1]
            flow_content += "=" * ((4 - len(flow_content) % 4) % 4)
            decoded_value = base64.b64decode(flow_content)
            print(decoded_value)
            with gzip.GzipFile(fileobj=io.BytesIO(decoded_value), mode="rb") as f:
                output.append(f.read().decode("utf-8"))
        logging.info(f'Output: {str(output)}')
        print(f'Contact Flow Names: {flow_names}')

        index = 0
        for flow in output:
            flow_json = json.loads(flow)
            print(str(flow_json))
            response = create_contact_flow(
                instance_id=instance_id, 
                name=flow_names[index], 
                type='CONTACT_FLOW',
                content=flow_json)
            print(f'Boto response: {response}')

    except Exception as ex:
        print(f'Error: {str(ex)}')

def create_contact_flow(instance_id, name, type, content):
    return connect_client.create_contact_flow(
        InstanceId=instance_id,
        Name=name,
        Type=type,
        Content=content
    )         

def get_object(bucket, key):
    return s3_client.get_object(
        Bucket=bucket,
        Key=key
    )
        