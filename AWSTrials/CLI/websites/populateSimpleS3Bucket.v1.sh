. ../aws_env_setup.sh

. ./env.sh


echo
echo $SHELL at $(date)

MY_BUCKET="${SIMPLE_S3_BUCKET_NAME}"

echo
echo "S3 bucket is ${MY_BUCKET}"
echo "Bucket region is ${BUCKET_REGION}"
echo "Source files are under ${SIMPLE_SITE_FILES}"

if [[ -z "${MY_BUCKET}" ]]
then
	echo "Bucket name not defined"
	exit 1
fi

echo
echo "List buckets:"
echo

aws s3api list-buckets

echo
echo "Delete ${MY_BUCKET} bucket, may not exist:"
echo

aws s3api delete-object --bucket "${MY_BUCKET}" --key index.html
aws s3api delete-object --bucket "${MY_BUCKET}" --key page2.html
aws s3api delete-object --bucket "${MY_BUCKET}" --key pngs/NG_1x1_red.png 

aws s3api delete-bucket --bucket "${MY_BUCKET}"

echo
echo "Create new ${MY_BUCKET} bucket in ${BUCKET_REGION} region:"
echo

aws s3api create-bucket --bucket "${MY_BUCKET}" --region ${BUCKET_REGION} --create-bucket-configuration LocationConstraint=${BUCKET_REGION}

echo
echo "Copy files to the bucket:"
echo

# NB Need to specify a content-type, otherwise files take on binary/octet-stream as their type, and don't work properly on a website.

aws s3api put-object --bucket "${MY_BUCKET}" --key index.html --content-type "text/html" --body ${SIMPLE_SITE_FILES}/index.html 
aws s3api put-object --bucket "${MY_BUCKET}" --key page2.html --content-type "text/html" --body ${SIMPLE_SITE_FILES}/page2.html 
aws s3api put-object --bucket "${MY_BUCKET}" --key pngs/NG_1x1_red.png --content-type "image/png" --body ${SIMPLE_SITE_FILES}/pngs/NG_1x1_red.png

echo
echo "List objects in the new bucket:"
echo

aws s3api list-objects --bucket "${MY_BUCKET}"

