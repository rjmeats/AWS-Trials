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

echo
echo "Get trace summaries:"
echo

EPOCH=$(date +%s)
aws xray get-trace-summaries --start-time $(($EPOCH-120)) --end-time $(($EPOCH-60))

