. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List subscriptions:"
echo

aws sns list-subscriptions

