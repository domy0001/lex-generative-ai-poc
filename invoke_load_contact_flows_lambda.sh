#!/bin/bash
load_lambda_name="load_contact_flows_lambda"
contact_flows_bucket_name="contact-flows-bucket"

value=""
json_dir="files"

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

aws lambda invoke \
    --function-name $load_lambda_name \
    --region eu-central-1 \
    --payload   '{
                    "input": "'"$value"'",
                    "bucket_name": "'"$contact_flows_bucket_name"'"
                }' \
    --cli-binary-format raw-in-base64-out \
    invoke_repsonse.json