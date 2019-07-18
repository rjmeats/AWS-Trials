. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Caller identity:"
echo

aws sts get-caller-identity

if [[ -z "${MY_ACCOUNT}" ]]
then
	echo
	echo "MY_ACCOUNT not defined"
	exit 1
fi

ARN="arn:aws:iam::${MY_ACCOUNT}:role/testSNSLambdaRole"

echo
echo "Assume role $ARN:"
echo

# Fails as this is a service role

aws sts assume-role --role-arn "${ARN}" --role-session-name "My-role-session"


