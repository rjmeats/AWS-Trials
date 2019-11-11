#########################################################

function getNBStatus () {
	local NB="$1"
	STATUS=$(aws sagemaker describe-notebook-instance --notebook-instance-name ${NB} | jq -r '.NotebookInstanceStatus')
	echo ${STATUS}
}

#########################################################

