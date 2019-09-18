. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Describe load balancers:"
echo

aws elbv2 describe-load-balancers

echo
echo "Describe target groups:"
echo

aws elbv2 describe-target-groups

