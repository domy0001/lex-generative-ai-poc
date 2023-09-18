#!/bin/bash
json_dir="files/"

for jn_file in "$json_dir"/*.json do
    filename=$(basename -- "$json_file")
    key="${filename}"
    json_content=$(cat "$json_file")
    export "$key=$json_content"
    echo "$key"
done