. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List stacks:"
echo

aws cloudformation list-stacks

echo
echo "List exports:"
echo

aws cloudformation list-exports

echo
echo "List stack sets:"
echo

aws cloudformation list-stack-sets

