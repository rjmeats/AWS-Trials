. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

if [[ -z ${ACCOUNT_ID} ]]
then
	echo "No ACCOUNT_ID value in environment"
	exit 1
else
	echo "Using ACCOUNT_ID ${ACCOUNT_ID}"
fi

echo
echo "List budgets:"
echo

aws budgets describe-budgets --account-id ${ACCOUNT_ID}

