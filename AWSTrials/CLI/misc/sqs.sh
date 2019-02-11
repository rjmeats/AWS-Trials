. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List queues:"
echo

aws sqs list-queues

