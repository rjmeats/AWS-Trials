. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Describe volumes:"
echo

aws ec2 describe-volumes
