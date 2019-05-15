. ../../../CLI/aws_env_setup.sh

echo
echo $(date)

aws lambda add-permission --cli-input-json file://add_permission.json