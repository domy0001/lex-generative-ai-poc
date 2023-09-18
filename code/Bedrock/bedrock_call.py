import json


def lambda_handler(event, context):
    # TODO implement

    #parsed_json = json.loads(event)
    print(json.dumps(event))
    print("input transcription:" +  event['inputTranscript'])

    if len(event['inputTranscript']) == 0:
        contentType = "Mi dispiace, ma non ho compreso la sua domanda. Potrebbe essere più chiaro?"
    else:
        #Bedrock invocation    
        contentType = "Processato richiesta, individuata la risposta e inoltrata al cliente."
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