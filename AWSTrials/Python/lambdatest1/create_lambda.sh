. ../../CLI/aws_env_setup.sh

echo
echo $(date)

./zip_code.sh

export ROLE_ARN="arn:aws:iam::686915945833:role/service-role/testPython-role-4xolz5di"
aws lambda create-function --function-name testPython1 --runtime python3.7 --handler test1.lambda_handler --role "$ROLE_ARN" --zip-file fileb://test1.zip



