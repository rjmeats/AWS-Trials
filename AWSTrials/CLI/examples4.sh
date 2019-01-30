. ./aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List regions as JSON"
echo "===================="
echo
echo "- first 20 lines"
echo
aws ec2 describe-regions --output json | head -20

echo
echo "List regions as text"
echo "===================="
echo
echo "- first 20 lines"
echo
aws ec2 describe-regions --output text | head -20


echo
echo "List regions as table"
echo "====================="
echo
echo "- first 20 lines"
echo
aws ec2 describe-regions --output table | head -20

# See http://jmespath.org/tutorial.html for the JSON query syntax

echo
echo "List regions as JSON - display first region only"
echo "================================================"
echo
aws ec2 describe-regions --output json --query 'Regions[0]'  


echo
echo "List regions as table - display third region only"
echo "================================================="
echo
aws ec2 describe-regions --output table --query 'Regions[2]'  


echo
echo "List regions as text - display third and fourth regions"
echo "======================================================="
echo
aws ec2 describe-regions --output text --query 'Regions[2:4]'  

echo
echo "List a subset of availability zone fields as json"
echo "================================================="
echo
aws ec2 describe-availability-zones --query 'AvailabilityZones[*].{Region:RegionName, Zone:ZoneName, ID:ZoneId}'

echo
echo "List a subset of availability zone fields as json, for a specific zone ID"
echo "========================================================================="
echo
aws ec2 describe-availability-zones --query 'AvailabilityZones[?ZoneId==`euw2-az3`].{Region:RegionName, Zone:ZoneName, ID:ZoneId}'


