. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List metrics:"
echo

aws cloudwatch list-metrics

echo
echo "Describe log groups:"
echo

aws logs describe-log-groups


echo
echo "List event rules:"
echo

aws events list-rules 

