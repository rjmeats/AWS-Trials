. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Describe clusters:"
echo

aws dax describe-clusters --region eu-west-1
