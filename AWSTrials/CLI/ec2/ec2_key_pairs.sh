. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Describe EC2 Key Pairs:"
echo

aws ec2 describe-key-pairs

echo
echo "Create an EC2 Key Pair:"
echo

aws ec2 create-key-pair --key-name "kpfromcli"

echo
echo "Describe EC2 Key Pairs:"
echo

aws ec2 describe-key-pairs

echo
echo "Delete an EC2 Key Pair:"
echo

aws ec2 delete-key-pair --key-name "kpfromcli"

echo
echo "Describe EC2 Key Pairs:"
echo

aws ec2 describe-key-pairs

