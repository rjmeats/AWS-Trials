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
echo "List models:"
echo

aws sagemaker list-models

echo
echo "List notebook instances:"
echo

aws sagemaker list-notebook-instances


echo
echo "List algorithms:"
echo

aws sagemaker list-algorithms

echo
echo "List endpoints:"
echo

aws sagemaker list-endpoints

echo
echo "List endpoint configs:"
echo

aws sagemaker list-endpoint-configs

echo
echo "List code repositories:"
echo

aws sagemaker list-code-repositories

echo
echo "List training jobs:"
echo

aws sagemaker list-training-jobs

echo
echo "List tuning jobs"
echo

aws sagemaker list-hyper-parameter-tuning-jobs

echo
echo "List labelling jobs:"
echo

aws sagemaker list-labeling-jobs

echo
echo "List transform jobs:"
echo

aws sagemaker list-transform-jobs

echo
echo "List compliation jobs:"
echo

aws sagemaker list-compilation-jobs

