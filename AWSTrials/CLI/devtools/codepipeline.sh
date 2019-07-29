. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List pipelines:"
echo

aws codepipeline list-pipelines

sleep 3

echo
echo "List action types:"
echo

aws codepipeline list-action-types

