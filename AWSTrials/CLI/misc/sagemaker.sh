. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

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
echo "List training jobs:"
echo

aws sagemaker list-training-jobs


echo
echo "List endpoints:"
echo

aws sagemaker list-endpoints

echo
echo "List labelling jobs:"
echo

aws sagemaker list-labeling-jobs

echo
echo "List transform jobs:"
echo

aws sagemaker list-transform-jobs

echo
echo "List code repositories:"
echo

aws sagemaker list-code-repositories

