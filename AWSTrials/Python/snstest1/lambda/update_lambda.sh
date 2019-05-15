. ../../../CLI/aws_env_setup.sh

echo
echo $(date)

./zip_code.sh

aws lambda update-function-code --function-name testPythonSNS --zip-file fileb://test1.zip



