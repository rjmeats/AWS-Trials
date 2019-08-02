. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List users:"
echo

aws iam list-users

echo
echo "List roles:"
echo

aws iam list-roles


echo
echo "List groups:"
echo

aws iam list-groups


echo
echo "List policies:"
echo

aws iam list-policies

