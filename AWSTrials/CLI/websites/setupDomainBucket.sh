. ../aws_env_setup.sh

. ./env.sh


echo
echo $SHELL at $(date)

MY_BUCKET="${DOMAIN_S3_BUCKET_NAME}"

echo
echo "S3 bucket is ${MY_BUCKET}"
echo "Bucket region is ${BUCKET_REGION}"
echo "Source files are under ${SIMPLE_SITE_FILES}"

if [[ -z "${MY_BUCKET}" ]]
then
	echo "Bucket name not defined"
	exit 1
fi

# Tell S3 to treat this bucket as a website

TMP_CFG_FILE=site.cfg.$$

# Here document to specify website config info
cat > ${TMP_CFG_FILE} << EOF
{
	"IndexDocument": {
		"Suffix": "index.html"
	}
}
EOF

echo
echo "Tell S3 that this bucket is a website"
echo

aws s3api put-bucket-website --bucket ${MY_BUCKET} --website-configuration file://${TMP_CFG_FILE}

rm ${TMP_CFG_FILE}

echo
echo "Show bucket website info"
echo
aws s3api get-bucket-website --bucket ${MY_BUCKET}


# Tell S3 to make this public publically readable

TMP_CFG_FILE=policy.cfg.$$

# Here document to specify website config info
cat > ${TMP_CFG_FILE} << EOF
{
	"Version":"2012-10-17",
	"Statement":[{
		"Sid":"PublicReadGetObject",
		"Effect":"Allow",
		"Principal": "*",
		"Action":["s3:GetObject"],
		"Resource":["arn:aws:s3:::${MY_BUCKET}/*"
		]
	}
	]
}
EOF

echo
echo "Tell S3 to use a public access policy for the bucket"
echo

aws s3api put-bucket-policy --bucket ${MY_BUCKET} --policy file://${TMP_CFG_FILE}

rm ${TMP_CFG_FILE}

echo
echo "Show bucket policy"
echo
aws s3api get-bucket-policy --bucket ${MY_BUCKET}


