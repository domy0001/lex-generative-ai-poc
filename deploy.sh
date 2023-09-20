#!/bin/bash
zip_dir="code/zip"
create_contact_flows_path="code/create_contact_flows/*"
bedrock_path="code/bedrock_env/*"
langchain_path="code/langchain_env/*"
load_flows_path="code/load_contact_flows/*"

if [ ! -d "$zip_dir" ]; then
    mkdir -p "$zip_dir"
    echo "Directory created: $zip_dir"
else
    echo "Directory already exists: $zip_dir"
fi

cd code/create_contact_flows
zip -r -D ../zip/create_contact_flows.zip *
cd ../bedrock_env
zip -r -D ../zip/bedrock.zip *
cd ../langchain_env
zip -r -D ../zip/langchain.zip *
cd ../load_contact_flows
zip -r -D ../zip/load_contact_flows.zip *
cd ../../

json_dir="files"
key="contact_flows"
value=""
for json_path_file in $json_dir/*.json;
do
    file_name=$(basename $json_path_file | cut -d. -f1)
    if [ -f $json_file_path]; then
        if [ -z $value]; then
            value=$file_name-$(cat "$json_path_file" | jq -c | jq -R | gzip -c | base64)
        else
            value=$file_name-$value:$(cat "$json_path_file" | jq -c | jq -R | gzip -c | base64)
        fi
    fi
done

echo $value > files/contact_flows.txt

load_lambda_name="load_contact_flows_lambda"
contact_flows_bucket_name="contact-flows-bucket"
sam build
sam package
sam validate

sam deploy --parameter-overrides LoadLambdaName=$load_lambda_name ContactFlowsBucketName=$contact_flows_bucket_name 

invoke_lambda_payload='{
    "input": "'$value'",
    "bucket_name": "'$contact_flows_bucket_name'"
}'

aws lambda invoke \
    --function-name $load_lambda_name \
    --region eu-central-1 \
    --payload $invoke_lambda_payload \
    --cli-binary-format raw-in-base64-out \
    invoke_repsonse.json