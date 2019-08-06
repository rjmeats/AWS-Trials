. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List distributions:"
echo

aws cloudfront list-distributions

