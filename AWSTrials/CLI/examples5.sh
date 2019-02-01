. ./aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List regions as JSON"
echo "===================="
echo
aws ec2 describe-regions --output json 

echo
echo "List the availability zones for the default region"
echo "=================================================="
echo
aws ec2 describe-availability-zones 

echo
echo "List the availability zones for the us-east-2 region"
echo "===================================================="
echo
aws ec2 describe-availability-zones --region us-east-2 

echo
echo "List the availability zones in 'available' state for the default region"
echo "======================================================================="
echo
echo "- displayed as a table"
echo
aws ec2 describe-availability-zones --filters Name=state,Values=available --output table

