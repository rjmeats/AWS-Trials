. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Subscription state:"
echo

aws shield get-subscription-state --region us-east-1
