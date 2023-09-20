json_dir="./../files"
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
echo $parameter_overrides_string | tee input.txt