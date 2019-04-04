. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List Cognito user pools:"
echo

aws cognito-idp list-user-pools --max-results 20

