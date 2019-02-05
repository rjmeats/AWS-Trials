. ./aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Account atttribues:"
echo

aws ec2 describe-account-attributes

