. ./aws_env_setup.sh

echo
echo $SHELL at $(date)

JSON='
[
	{
		"Name": "instance-type",
		"Values": ["t2.micro", "m1.medium"]
	},
	{
		"Name": "availability-zone",
		"Values": ["us-west-2c"]
	}
]
'

echo
echo "JSON parameter on the command line"
echo "=================================="
echo

aws ec2 describe-instances --filters "${JSON}" 

echo
echo "JSON parameter from a file"
echo "=========================="
echo

FILENAME="json.$$.txt"

echo "$JSON" > ${FILENAME}

aws ec2 describe-instances --filters file://${FILENAME} 

rm ${FILENAME}


echo
echo "Generate a CLI JSON skeleton"
echo "============================"
echo
aws ec2 describe-instances --generate-cli-skeleton > ${FILENAME}

cat $FILENAME

echo
echo "Run using CLI JSON skeleton file"
echo "================================"
echo
echo - NB AWS reports a missing parameter error as we have not filled in the JSON skeleton with values.

aws ec2 describe-instances --cli-input-json file://${FILENAME}

rm ${FILENAME}

