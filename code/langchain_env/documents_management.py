import boto3
import json

bedrock = boto3.client('bedrock', 'region')
model_id= 'amazon.titan-tg1-large'

def handler(event, context):
    lex_input = event['inputTranscript']
    content_type = 'application/json'
    accept = 'application/json'
    request_body = json.dumps({"inputText": lex_input})

    try:
        response = bedrock.invoke_model(body=request_body, modelId=model_id, accept=accept, contentType=content_type)
        response_body = json.loads(response.get('body').read())
        return response_body.get('results')[0].get('outputText')
    except Exception as ex:
        print(ex)
