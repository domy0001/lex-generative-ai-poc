import os
import json
import boto3
from botocore.config import Config

bedrock_region = os.environ['BEDROCK_REGION']
account_id = os.environ['ACCOUNT_ID']
bedrock_endpoint = os.environ['BEDROCK_ENDPOINT']
model_id = "amazon.titan-tg1-large"
boto3_kwargs = {}
boto3_kwargs['endpoint_url']=bedrock_endpoint

config = Config(
        region_name = bedrock_region,
        retries = {
            'max_attempts' : 10,
            'mode' : 'standard'
        }
    )

bedrock_client = boto3.client(
        service_name='bedrock',
        config=config,
        region_name=bedrock_region,
        **boto3_kwargs
    )

parameters = {
        "maxTokenCount":10,
        "stopSequences":[],
        "temperature":0,
        "topP":0.9
    }

accept = "application/json"
content_type = "application/json"

def get_response(input_text, model_id, accept, content_type):
    body = json.dumps({"inputText" : input_text, "textGenerationConfig" : parameters})
    response = bedrock_client.invoke_model(body=body, modelId=model_id, accept=accept, contentType=content_type)
    response_body = json.loads(response.get('body').read())
    return response_body.get("results")[0].get("outputText")


def handler(event, context):
    print(json.dumps(event))
    print("input transcription:" +  event['inputTranscript'])

    if len(event['inputTranscript']) == 0:
        contentType = "Mi dispiace, ma non ho compreso la sua domanda. Potrebbe essere più chiaro?"
    else:
        #Bedrock invocation    
        contentType = get_response(
            input_text=event['inputTranscript'],
            model_id=model_id,
            accept=accept, 
            content_type=content_type)

    return {
       'sessionState': {
            'sessionAttributes': None,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': {
                'name': 'FallbackIntent',
                'state': 'Fulfilled'
            }
        },
        'messages': [
            {
                'contentType': 'PlainText','content': contentType
            }
        ] 
    }
