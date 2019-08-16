. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List state machines:"
echo

aws stepfunctions list-state-machines
