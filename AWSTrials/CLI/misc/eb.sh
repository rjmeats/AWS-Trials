. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Check DNS availability:"
echo

aws elasticbeanstalk check-dns-availability --cname-prefix abcd 

echo
echo "Check DNS availability:"
echo

aws elasticbeanstalk check-dns-availability --cname-prefix rjrj 

echo
echo "Describe applications:"
echo

aws elasticbeanstalk describe-applications

echo
echo "Describe environments:"
echo

aws elasticbeanstalk describe-environments


echo
echo "Describe account attributes:"
echo

aws elasticbeanstalk describe-account-attributes

