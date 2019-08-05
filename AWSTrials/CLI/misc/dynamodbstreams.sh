. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List streams:"
echo

aws dynamodbstreams list-streams
