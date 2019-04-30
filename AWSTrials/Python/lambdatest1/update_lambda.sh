. ../../CLI/aws_env_setup.sh

echo
echo $(date)

./zip_code.sh

aws lambda update-function-code --function-name testPython1 --zip-file fileb://test1.zip



