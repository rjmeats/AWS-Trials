. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List console login events:"
echo

aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=ConsoleLogin

