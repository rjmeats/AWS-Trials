. ./aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List services names from pricing data"
echo "====================================="
echo

aws pricing describe-services --endpoint-url https://api.pricing.us-east-1.amazonaws.com --region us-east-1 --query 'Services[*].{ServiceCode:ServiceCode}' --output text | sort | dos2unix



