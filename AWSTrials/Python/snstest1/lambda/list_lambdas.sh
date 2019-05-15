. ../../../CLI/aws_env_setup.sh

echo
echo $(date)

aws lambda list-functions --output text  | grep -i sns
 
aws lambda get-policy --function-name "testPythonSNS1"

