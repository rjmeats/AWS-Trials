. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List secrets:"
echo

aws secretsmanager list-secrets

