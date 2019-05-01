. ../../CLI/aws_env_setup.sh

echo
echo $(date)
echo

OUTFILE="invoke.out.txt"

PAYLOAD='{ "a": 225, "b": "abc.2", "d" : "aaxxx.2" }'

aws lambda invoke --function-name testPython2 --payload "$PAYLOAD" $OUTFILE

echo
echo Lambda output
echo

cat $OUTFILE | jq

rm -f ${OUTFILE}

