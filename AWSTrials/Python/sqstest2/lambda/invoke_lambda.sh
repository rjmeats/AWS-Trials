. ../../../CLI/aws_env_setup.sh

echo
echo $(date)
echo

OUTFILE="invoke.out.txt"

PAYLOAD='{ "a": 25, "b": "abc", "d" : "aaxxx" }'

aws lambda invoke --function-name testPythonSQS --payload "$PAYLOAD" $OUTFILE

echo
echo Lambda output
echo

cat $OUTFILE | jq

rm -f ${OUTFILE}

