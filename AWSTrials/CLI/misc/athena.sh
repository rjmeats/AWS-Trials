. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List named queries:"
echo

aws athena list-named-queries

echo
echo "List query executions:"
echo

aws athena list-query-executions

echo
echo "List work groups:"
echo

aws athena list-work-groups

