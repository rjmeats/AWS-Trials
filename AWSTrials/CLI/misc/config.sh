. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Describe config rules:"
echo

aws configservice describe-config-rules
