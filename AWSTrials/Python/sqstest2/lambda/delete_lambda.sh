. ../../../CLI/aws_env_setup.sh

echo
echo $(date)

aws lambda delete-function --function-name testPythonSQS


