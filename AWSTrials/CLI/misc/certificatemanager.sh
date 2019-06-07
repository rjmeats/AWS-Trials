. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List certificates:"
echo

aws acm list-certificates --region us-east-1

echo
echo "Describe certificates:"
echo

for c in `aws acm list-certificates --region us-east-1 --output text | cut -f2`
do
	echo Certificate $c
	echo
	aws acm describe-certificate --certificate-arn "$c" --region us-east-1
	echo
	echo "Get ... "
	echo
	aws acm get-certificate --certificate-arn "$c" --region us-east-1
done

