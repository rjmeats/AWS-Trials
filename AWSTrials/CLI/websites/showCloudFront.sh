. ../aws_env_setup.sh

. ./env.sh


echo
echo $SHELL at $(date)

echo
echo "Listing CloudFront distributions"
echo

aws cloudfront list-distributions

