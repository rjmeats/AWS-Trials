. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

if [[ ! -z "$1" ]]
then
	REGION="$1"
	echo
	echo "Setting default region to $REGION"
	export AWS_DEFAULT_REGION="${REGION}"
fi

echo
echo "List notebook instances:"
echo

aws sagemaker list-notebook-instances


