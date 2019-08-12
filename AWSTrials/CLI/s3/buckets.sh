. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List buckets:"
echo

aws s3api list-buckets

MY_BUCKET="rjm-cli-test-bucket"

echo
echo "Delete ${MY_BUCKET} bucket, may not exist:"
echo

aws s3api delete-bucket --bucket "${MY_BUCKET}"

echo
echo "Create new ${MY_BUCKET} bucket:"
echo
echo "- in London region"
echo

aws s3api create-bucket --bucket "${MY_BUCKET}" --region eu-west-2 --create-bucket-configuration LocationConstraint=eu-west-2

echo
echo "List buckets:"
echo

aws s3api list-buckets

echo
echo "Display ${MY_BUCKET} info:"
echo

aws s3api get-bucket-cors --bucket "${MY_BUCKET}" --region eu-west-2


echo
echo "Try to create ${MY_BUCKET} bucket again:"
echo
echo "- expect an 'already exists and you own it' error"
echo

aws s3api create-bucket --bucket "${MY_BUCKET}" --region eu-west-2 --create-bucket-configuration LocationConstraint=eu-west-2


echo
echo "Try to create 'rjm' bucket again:"
echo
echo "- expect an 'can't create, already exists' error, not owned by me"
echo

aws s3api create-bucket --bucket rjm --region eu-west-2 --create-bucket-configuration LocationConstraint=eu-west-2

echo
echo "Delete ${MY_BUCKET} bucket to tidy up:"
echo

aws s3api delete-bucket --bucket "${MY_BUCKET}"

echo
echo "List buckets:"
echo

aws s3api list-buckets
