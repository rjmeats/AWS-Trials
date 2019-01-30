. ./aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Top-level help text"
echo "==================="
echo
echo "- first 20 lines"
echo
aws help | head -20

echo
echo
echo "Help text for a specific command, e.g. ec2"
echo "=========================================="
echo
echo "- first 20 lines"
echo
aws ec2 help | head -20


echo
echo
echo "Help text for an option of a specific command, e.g. iam list-users"
echo "=================================================================="
echo
echo "- first 20 lines"
echo
aws iam list-users help | head -20


