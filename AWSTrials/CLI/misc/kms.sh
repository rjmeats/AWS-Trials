. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "List keys:"
echo

aws kms list-keys

echo
echo "List aliases:"
echo

aws kms list-aliases

echo
echo "Describe keys:"
echo

for k in `aws kms list-keys --output text | cut -f2`
do
	echo Key $k
	echo
	aws kms describe-key --key-id "$k"
done

