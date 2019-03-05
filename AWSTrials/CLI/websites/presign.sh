. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Presign S3 object:"
echo

aws s3 presign s3://rjm-simple-web-site1/index.html

echo
echo "Presign S3 object with expiry in 120 seconds:"
echo

aws s3 presign s3://rjm-simple-web-site1/index.html --expires-in 120

echo
echo "Presign S3 private object with expiry in 120 seconds:"
echo

aws s3 presign s3://rjm-private/extra.html --expires-in 120
