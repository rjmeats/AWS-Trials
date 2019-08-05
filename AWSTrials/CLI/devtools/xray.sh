. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List sampling rules:"
echo

aws xray get-sampling-rules

echo
echo "List groups:"
echo

aws xray get-groups

