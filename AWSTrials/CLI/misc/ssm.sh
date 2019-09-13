. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Describe parameters:"
echo

aws ssm describe-parameters

