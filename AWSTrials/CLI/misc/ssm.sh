. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Describe parameters:"
echo

aws ssm describe-parameters


echo
echo "List Amazon Linux Parameter Store namespaces:"
echo
echo "for the default region"
echo

# NB Doesn't run properly when run direct from Bash - not clear why, puts a C:\..... prefix onto path !

powershell 'aws ssm get-parameters-by-path --path "/aws/service/ami-amazon-linux-latest"'


