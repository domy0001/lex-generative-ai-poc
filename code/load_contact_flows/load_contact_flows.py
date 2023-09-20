import boto3

client = boto3.client('s3')

def handler(event, context):
    print(event)
    encoded_input_bytes = bytes(event['input'], 'utf-8')
    bucket_name = event['bucket_name']
    object_key = "encoded_contact_flows.txt"

    try:
        client.put_object(
            Body=encoded_input_bytes,
            Bucket=bucket_name,
            Key=object_key
        )
    except Exception as ex:
        print(f'Error: {ex}')
