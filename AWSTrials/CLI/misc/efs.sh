. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Describe file systems:"
echo

aws efs describe-file-systems
