. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List APIs:"
echo

aws apigatewayv2 get-apis

