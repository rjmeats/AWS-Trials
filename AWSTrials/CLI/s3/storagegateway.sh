. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Gateways:"
echo

aws storagegateway list-gateways 


echo
echo "Volumes:"
echo

aws storagegateway list-volumes 


echo
echo "Tapes:"
echo

aws storagegateway list-tapes 


echo
echo "File shares:"
echo

aws storagegateway list-file-shares 

