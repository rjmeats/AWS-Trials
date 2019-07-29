. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List environments:"
echo

aws cloud9 list-environments --region eu-west-1


echo
echo "Describe environments:"
echo

ENVIDS=$(aws cloud9 list-environments --region eu-west-1 --output text | cut -f2)

echo $ENVIDS

aws cloud9 describe-environments --region eu-west-1 --environment-ids "${ENVIDS}"

