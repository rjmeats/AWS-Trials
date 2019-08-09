. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Show account settings:"
echo

aws lambda get-account-settings

echo
echo "List functions:"
echo

aws lambda list-functions
