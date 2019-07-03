. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List repositories:"
echo

aws codecommit list-repositories

echo
echo "Create repository:"
echo

aws codecommit create-repository --repository-name test-repo1

echo
echo "List repositories:"
echo

aws codecommit list-repositories

echo
echo "Make local clone"
echo
echo "NB asks for credentials"
echo

git clone "https://git-codecommit.eu-west-2.amazonaws.com/v1/repos/test-repo1"

ls -ltr

echo
echo "Delete repository:"
echo

aws codecommit delete-repository --repository-name test-repo1

echo
echo "List repositories:"
echo

aws codecommit list-repositories

