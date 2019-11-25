. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

TSTART=2019-11-22
TEND=2019-11-24
GRANULARITY=DAILY

if [[ ! -z $1 && ! -z $2 ]]
then
	TSTART="$1"
	TEND="$2"

	if [[ ! -z $3 ]]
	then
		GRANULARITY="$3"
	fi
fi

echo "Showing costs and usage for $TSTART (inclusive) to $TEND (exclusive), granularity $GRANULARITY"

# https://docs.aws.amazon.com/cli/latest/reference/ce/get-cost-and-usage.html

aws ce get-cost-and-usage \
	--time-period Start="${TSTART}",End="${TEND}" \
	--granularity DAILY \
	--metrics "BlendedCost" "UnblendedCost" "UsageQuantity" \
	--group-by Type=DIMENSION,Key=SERVICE Type=DIMENSION,Key=OPERATION 

