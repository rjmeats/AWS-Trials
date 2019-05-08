. ../../../CLI/aws_env_setup.sh

echo
echo $(date)

./zip_code.sh

ROLE_ARN="arn:aws:iam::686915945833:role/service-role/testSQSLambdaRole"

aws lambda create-function --function-name testPythonSQS --runtime python3.7 --handler test1.lambda_handler --role "$ROLE_ARN" --zip-file fileb://test1.zip \
	--environment "Variables={MYVAR1=10,MYVAR2=abc}"



