. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List tables:"
echo

aws dynamodb list-tables

echo
echo "List global tables:"
echo

aws dynamodb list-global-tables


echo
echo "Describe table:"
echo

aws dynamodb describe-table --table-name ddb_test_table1
