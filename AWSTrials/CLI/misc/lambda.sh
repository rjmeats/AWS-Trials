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

echo
echo "List aliases:"
echo

aws lambda list-aliases --function-name HelloWorldLambda

echo
echo "List event source mappings:"
echo

aws lambda list-event-source-mappings
