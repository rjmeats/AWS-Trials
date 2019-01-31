. ./aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List regions as JSON"
echo "===================="
echo
aws ec2 describe-regions --output json 

echo
echo "Just list region names as text"
echo "=============================="
echo

aws ec2 describe-regions --output text --query 'Regions[*].{Name:RegionName}'  | sort

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

echo
echo "List the availability zones for each region in turn"
echo "==================================================="
echo

REGION_LIST=$(aws ec2 describe-regions --output text --query 'Regions[*].{Name:RegionName}'  | dos2unix | sort)
for REGION in ${REGION_LIST}
do
	# echo "Found region $REGION"
	aws ec2 describe-availability-zones --region "${REGION}" --output text | dos2unix | sort
done 

