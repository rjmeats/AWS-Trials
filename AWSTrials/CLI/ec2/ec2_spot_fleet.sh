. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Describe spot fleets:"
echo

aws ec2 describe-fleets

