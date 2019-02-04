. ./aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Region names:"
echo

aws ec2 describe-regions --output text --query 'Regions[*].{Name:RegionName}'  | sort

echo
echo "Availability zones for each region:"
echo
echo "- NB AZ Name-to-ID mapping can vary from account to account!"

# --output text Columns seem to be returned in alphabetical order of the column name, regardless of order in the --query parameter
printf "%s\t\t%s\t\t%s\t\t%s\n" "Region" "State" "Zone Id" "Zone Name"

REGION_LIST=$(aws ec2 describe-regions --output text --query 'Regions[*].{Name:RegionName}'  | dos2unix | sort)
for REGION in ${REGION_LIST}
do
	# echo "Found region $REGION"
	aws ec2 describe-availability-zones --region "${REGION}" --query 'AvailabilityZones[*].{RegionName:RegionName,State:State,ZoneName:ZoneName,ZoneId:ZoneId}' --output text | dos2unix | sort
done 

