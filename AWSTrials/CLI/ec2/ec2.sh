. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Describe instances:"
echo

aws ec2 describe-instances
