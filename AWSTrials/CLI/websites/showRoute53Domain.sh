. ../aws_env_setup.sh

. ./env.sh


echo
echo $SHELL at $(date)

MY_DOMAIN="${DOMAIN_S3_BUCKET_NAME}"

echo
echo "Domain is ${MY_DOMAIN}"

if [[ -z "${MY_DOMAIN}" ]]
then
	echo "Domain name not defined"
	exit 1
fi

echo
echo "Listing hosted zones"
echo

aws route53 list-hosted-zones

# Capture the ID for this zone

ZONEID=$(aws route53 list-hosted-zones --output text | grep $MY_DOMAIN | cut -f3)

echo "Zone ID is [${ZONEID}]"

echo
echo "Showing hosted zone"
echo

aws route53 get-hosted-zone --id $ZONEID

echo
echo "Showing record sets"
echo

aws route53 list-resource-record-sets --hosted-zone-id $ZONEID
