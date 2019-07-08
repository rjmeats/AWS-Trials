. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List environment docker images:"
echo

aws codebuild list-curated-environment-images

echo
echo "List build projects:"
echo

aws codebuild list-projects

