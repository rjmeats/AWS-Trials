. ../../CLI/aws_env_setup.sh

echo
echo $(date)
echo

OUTFILE="invoke.out.txt"

PAYLOAD='10.34'

aws lambda invoke --function-name testPython1 --payload "$PAYLOAD" $OUTFILE

echo
echo Lambda output
echo

cat $OUTFILE | jq

rm -f ${OUTFILE}

