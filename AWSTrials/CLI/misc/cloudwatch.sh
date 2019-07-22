. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List metrics:"
echo

aws cloudwatch list-metrics

