BAD_PARAMETERS=N

if [[ ! -z "$1" ]]
then
	REGION="$1"
	echo
	echo "Setting default region to $REGION"
	export AWS_DEFAULT_REGION="${REGION}"

	if [[ ! -z "$2" ]]
	then
		NOTEBOOK="$2"
		# echo
		# echo "Using notebook $NOTEBOOK"
	else
		BAD_PARAMETERS=Y
		echo
		echo "No notebook specified"	
	fi
else
	BAD_PARAMETERS=Y
	echo
	echo "No region specified"
fi

if [[ $BAD_PARAMETERS == "Y" ]]
then
	echo
	echo "Usage is $0 <region> <notebookname>"
	echo
	exit 1
fi

. ../aws_env_setup.sh
. ./nb_functions.sh

echo
echo "Details of Notebook instance $NOTEBOOK :"
echo

aws sagemaker describe-notebook-instance --notebook-instance-name $NOTEBOOK

if [[ $? -ne 0 ]]
then
	echo
	echo "Error describing notebook $NOTEBOOK"
	echo
	exit 1
fi

echo
while [[ : ]]
do
	sleep 3
	NBSTATUS=$(getNBStatus $NOTEBOOK)
	T=`date`
	echo "$T : Status is $NBSTATUS ..."
done


