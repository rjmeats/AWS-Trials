. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List Cognito user pools:"
echo

aws cognito-idp list-user-pools --max-results 20

echo
echo "List Cognito identity pools:"
echo

aws cognito-identity list-identity-pools --max-results 20

