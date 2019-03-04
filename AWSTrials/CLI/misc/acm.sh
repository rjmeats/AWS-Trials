. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List certificates:"
echo
echo "- US East 1 (North Virginia) region"
echo 

aws acm list-certificates --region us-east-1

CERT_ARN=$(aws acm list-certificates --region us-east-1 --output text | cut -f2)

echo
echo "Describe certificate:"
echo
echo "- US East 1 (North Virginia) region"
echo "- ARN: $CERT_ARN"
echo 

aws acm describe-certificate --region us-east-1 --certificate-arn $CERT_ARN

echo
echo "Get certificate:"
echo
echo "- US East 1 (North Virginia) region"
echo "- ARN: $CERT_ARN"
echo 

aws acm get-certificate --region us-east-1 --certificate-arn $CERT_ARN

