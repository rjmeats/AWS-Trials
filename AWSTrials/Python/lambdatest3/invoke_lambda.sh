. ../../CLI/aws_env_setup.sh

echo
echo $(date)
echo

OUTFILE="invoke.out.txt"

PAYLOAD='{ "site" : "https://www.reuters.com" }'

aws lambda invoke --function-name testPython3 --payload "$PAYLOAD" $OUTFILE

echo
echo Lambda output
echo

cat $OUTFILE | jq

rm -f ${OUTFILE}

