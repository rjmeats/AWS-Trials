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

