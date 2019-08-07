. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List stacks:"
echo

aws cloudformation list-stacks

