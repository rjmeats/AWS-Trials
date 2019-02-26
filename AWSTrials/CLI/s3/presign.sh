. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Presign S3 object:"
echo

aws s3 presign s3://rjm-simple-web-site1/index.html
