. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List clusters:"
echo

aws eks list-clusters
