# Setting aws as a command alias, and allow it to work in shell scripts
alias aws=aws.cmd
shopt -s expand_aliases

echo 
echo $SHELL at $(date)

echo
echo "Location of the aws command:"
echo "============================"
echo
where aws

echo
echo "AWS CLI version:"
echo "================"
echo
aws --version

echo
echo "AWS configuration settings:"
echo "==========================="
echo
echo "- default profile"
echo
aws configure list

echo
echo "- paris profile"
echo
aws configure list --profile paris

echo
echo "Display credentials file contents:"
echo "=================================="
echo
cat ~/.aws/credentials

echo
echo "Display config file contents:"
echo "============================="
echo
cat ~/.aws/config

echo
echo "Display users using the default profile:"
echo "========================================"
echo
aws iam list-users

echo
echo "... and using the AWS_DEFAULT_OUTPUT variable to change the output format to text"

echo
export AWS_DEFAULT_OUTPUT="text"
aws iam list-users
unset AWS_DEFAULT_OUTPUT

echo
echo "... and using the --profile option to specify the paris profile"
echo
aws iam list-users --profile paris

echo
echo "... and using the AWS_PROFILE environment variable to specify the paris profile"

echo
export AWS_PROFILE="paris"
aws iam list-users 
unset AWS_PROFILE


