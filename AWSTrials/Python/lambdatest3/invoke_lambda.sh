. ../../CLI/aws_env_setup.sh

echo
echo $(date)
echo

OUTFILE="invoke.out.txt"

if [[ -z $1 ]]
then
	SITE="https://www.reuters.com"
else
	SITE="$1"
fi

PAYLOAD="{ \"site\" : \"$SITE\" }"

echo $PAYLOAD

aws lambda invoke --function-name testPython3 --payload "$PAYLOAD" $OUTFILE

echo
echo Lambda output
echo

cat $OUTFILE | jq

rm -f ${OUTFILE}

