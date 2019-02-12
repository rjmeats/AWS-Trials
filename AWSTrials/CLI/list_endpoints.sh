. ./aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "VPC Endpoints available in the current region:"
echo

aws ec2 describe-vpc-endpoint-services --output text  | grep BASE

