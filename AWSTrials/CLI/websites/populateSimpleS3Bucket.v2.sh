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

aws s3 ls

echo
echo "Check if bucket already exists ..."

# head-bucket command produces an error message to stderr if the bucket does not exist. Capture that,
# but just use the return status to determine if the bucket exists or not.
E=$(aws s3api head-bucket --bucket ${MY_BUCKET} 2>&1)

if [[ $? -ne 0 ]]
then
	echo	
	echo "Bucket ${MY_BUCKET} does not exist - nothing to delete"
else
	echo
	echo "Bucket ${MY_BUCKET} exists - contents:"
	echo

	aws s3 ls s3://"${MY_BUCKET}" --recursive

	echo
	echo "Delete ${MY_BUCKET} bucket and contents"
	echo

	aws s3 rb s3://"${MY_BUCKET}" --force
fi

echo
echo "Create new ${MY_BUCKET} bucket in ${BUCKET_REGION} region:"
echo

aws s3api create-bucket --bucket "${MY_BUCKET}" --region ${BUCKET_REGION} --create-bucket-configuration LocationConstraint=${BUCKET_REGION}

echo
echo "Copy files to the bucket:"
echo

aws s3 cp "${SIMPLE_SITE_FILES}" s3://"${MY_BUCKET}" --recursive

echo
echo "List objects in the new bucket:"
echo

aws s3 ls s3://"${MY_BUCKET}" --recursive

echo

aws s3api list-objects --bucket "${MY_BUCKET}"

