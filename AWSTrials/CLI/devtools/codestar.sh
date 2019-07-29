. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List projects:"
echo

aws codestar list-projects

echo
echo "List user-profiles:"
echo

aws codestar list-user-profiles

