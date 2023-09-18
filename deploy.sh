#!/bin/bash
zip_dir="code/zip"
base_64_path="code/base_64_decode_env"
bedrock_path="code/bedrock_env"
langchain_path="code/langchain_env"

if [ ! -d "$zip_dir" ]; then
    mkdir -p "$zip_dir"
    echo "Directory created: $zip_dir"
else
    echo "Directory already exists: $zip_dir"
fi

zip -r code/zip/base_64_decode.zip $base_64_path
zip -r code/zip/bedrock.zip $bedrock_path
zip -r code/zip/langchain.zip $langchain_path

json_dir="files"
parameter_overrides=()

for json_path_file in $json_dir/*.json;
do
    if [ -f $json_file_path]; then
        f=$(basename -- "$json_path_file" .${json_path_file##*.}) 
        key=${f}
        json_content=$(cat "$json_path_file" | jq -c | jq -R | gzip -c | base64)
        parameter_overrides+=($key=$json_content)
    fi
done
parameter_overrides_string=$(IFS=  ; echo "${parameter_overrides[*]}")
sam build
sam package
sam deploy --parameter-overrides $parameter_overrides