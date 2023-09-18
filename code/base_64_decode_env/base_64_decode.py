import os
import zlib
import json
import base64
import cfnresponse

def handler(event, context):
    try:

        encoded_inputs = os.environ['BASE_64_INPUT_VALUES']
        encoded_inputs = encoded_inputs.split(':')
        output = []

        for enc_input in encoded_inputs:
            decoded_value = base64.b64decode(enc_input)
            decompr_value = zlib.decompress(decoded_value).decode('utf-8')
            output.append(decompr_value)

        cfnresponse.response(event, context, cfnresponse.SUCCESS, output)
    except Exception as ex:
        cfnresponse.response(event, context, cfnresponse.FAILED, {"Error": str(ex)})


        