. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List applications:"
echo

aws deploy list-applications

echo
echo "List deployments:"
echo

aws deploy list-deployments

