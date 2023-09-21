#!/bin/bash
load_lambda_name="load_contact_flows_lambda"
contact_flows_bucket_name="contact-flows-bucket"

create_dir="files/created"

if [ ! -d "$create_dir" ]; then
    mkdir -p "$create_dir"
    echo "Directory created: $create_dir"
else
    echo "Directory already exists: $create_dir"
fi

value=""
json_dir="files"
for json_path_file in $json_dir/*.json;
do  
    file_name=$(basename $json_path_file | cut -d. -f1)
    file_name_with_ext=$(basename $json_path_file)
    if [ -f $json_file_path ] && [ ! -f $json_dir/created/$file_name_with_ext ]; then
        if [ -z $value]; then
            value=$file_name-$(cat "$json_path_file" | jq -c | jq -R | gzip -c | base64)
        else
            value=$file_name-$value:$(cat "$json_path_file" | jq -c | jq -R | gzip -c | base64)
        fi
    fi
done

response=$(aws lambda invoke \
    --function-name $load_lambda_name \
    --region eu-central-1 \
    --payload   '{
                    "input": "'"$value"'",
                    "bucket_name": "'"$contact_flows_bucket_name"'"
                }' \
    --cli-binary-format raw-in-base64-out \
    invoke_repsonse.json \
)
for json_path_file in $json_dir/*.json;
do  
    filename=$(basename $json_path_file)
    cp $json_dir/$filename $json_dir/created/$filename
done

