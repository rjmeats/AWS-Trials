. ../../CLI/aws_env_setup.sh

echo
echo $(date)

./zip_code.sh

aws lambda update-function-code --function-name testPython3 --zip-file fileb://test3.zip



