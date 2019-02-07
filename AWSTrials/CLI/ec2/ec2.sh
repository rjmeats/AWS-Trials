. ../aws_env_setup.sh

echo
echo $SHELL at $(date)

echo
echo "Describe instances:"
echo

aws ec2 describe-instances

echo
echo "Describe AMI images from amazon:"
echo
echo "- just show the first 50 lines of vast amounts of output"
echo

aws ec2 describe-images --owners amazon | head -50
