import base64
import json
import gzip
import io

input_file = '../input.txt'

if __name__ == '__main__':
    text_file = open(input_file, 'r')
    encoded_inputs = text_file.read()
    encoded_inputs = encoded_inputs.split(':')
    output = []
    for enc_input in encoded_inputs:
        enc_input_split = enc_input.split("=")
        enc_input_split[1] += "=" * ((4 - len(enc_input_split[1]) % 4) % 4)
        decoded_value = base64.b64decode(enc_input_split[1])
        with gzip.GzipFile(fileobj=io.BytesIO(decoded_value), mode="rb") as f:
            output.append(f.read().decode("utf-8"))
    flow = output[0]
    obj = json.loads(flow)
    json_string = json.dumps(obj)
    print(json_string)

