. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List accounts:"
echo

aws organizations list-accounts

