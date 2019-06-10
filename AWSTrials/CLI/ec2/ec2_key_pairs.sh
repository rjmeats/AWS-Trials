. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Describe EC2 Key Pairs:"
echo

aws ec2 describe-key-pairs
